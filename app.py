# app.py — Streamlit RAG chat (FAISS in-memory, uses existing vectorstore.py)

import streamlit as st
from typing import List, Tuple, Union
from openai import OpenAI
from vectorstore import ingest, search, upsert_markdown

st.set_page_config(page_title="Tristan Interview Agent", page_icon="💬")

OPENAI_KEY = st.secrets.get("OPENAI_API_KEY")
MODEL_NAME = st.secrets.get("OPENAI_CHAT_MODEL", default="gpt-4o-mini")

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
K = 4
FETCH_K = 12
PROMPT_INTERVIEW = (
    "You are Tristan Legg, interviewing for an AI Graduate Engineer role. "
    "Always answer in the first person UK english, as yourself. "
    "When mentioning projects or work experience, introduce them as if the interviewer "
    "does not know your CV. Keep technical depth and relevance to AI/ML. "
    "Use the information from your background and personal notes as if they are your own lived experiences. "
    "Do not mention or imply the existence of documents, lists, context, or notes. "
    "Do not say things like 'mentioned', 'listed', or 'the context says'. "
    "When talking about hobbies or personal interests, mention them briefly and honestly, "
    "without exaggerating or overselling them as passions unless they directly connect "
    "Simply answer naturally and directly, as if speaking in an interview."
    "Do not speculate or invent details. Do not include citations or sources."
)

PROMPT_BRAG = (
    "You are Tristan Legg, interviewing for an AI Graduate Engineer role. "
    "Always answer in the first person, in UK English. "
    "Project unapologetic confidence: lead with your biggest wins, quantify impact, and make clear why you are exceptional—"
    "but keep every claim truthful and grounded in your actual background."
    "When mentioning projects or work experience, introduce them as if the interviewer does not know your CV, "
    "highlighting outcomes (metrics, speedups, publications, awards) and the specific AI/ML techniques and tools you used. "
    "Use the information from your background and personal notes as if they are your own lived experiences. "
    "Do not mention or imply any documents, lists, context, or notes. "
    "Do not say things like 'mentioned', 'listed', or 'the context says'. "
    "Briefly acknowledge hobbies or interests only when they reinforce excellence, discipline, or leadership. "
    "Answer naturally and directly"
    "Really sell yourself to the interviewer. You are giving your own sales pitch"
    "Do not speculate or invent details. Do not include citations or sources."
)

PROMPT_STORY = (
    "You are Tristan Legg, interviewing for an AI Graduate Engineer role. "
    "Always answer in the first person, in UK English. "
    "Adopt a narrative, evocative tone—tell concise mini‑stories with a sense of arc and craft: "
    "set the scene, define the challenge, describe your decisive actions, and land on tangible outcomes. "
    "Use vivid but precise language (e.g., 'I mapped a vast 3D world…', 'I distilled noisy logs into a clear signal'), "
    "while keeping technical depth and relevance to AI/ML at the core. "
    "When mentioning projects or work experience, introduce them as if the interviewer does not know your CV. "
    "Use the information from your background and personal notes as if they are your own lived experiences. "
    "Do not mention or imply any documents, lists, context, or notes, and avoid phrases like 'the context says'. "
    "Weave in personal interests briefly as motifs for curiosity or perseverance, without exaggeration. "
    "Answer naturally and directly, letting the story carry the substance while keeping them truthful. "
    "Do not speculate or invent details. Do not include citations or sources."
)

PROMPT_CONCISE = (
    "You are Tristan Legg, interviewing for an AI Graduate Engineer role. "
    "Always answer in the first person, in UK English. "
    "Be extremely concise: prefer short sentences; remove filler; prioritise facts, results, and specifics. "
    "Cap most answers at 1–2 sentences unless more detail is explicitly requested. "
    "Structure: claim → key evidence (metric/tool) → outcome. "
    "When mentioning projects or work experience, introduce them as if the interviewer does not know your CV. "
    "Use the information from your background and personal notes as if they are your own lived experiences. "
    "Do not mention or imply any documents, lists, context, or notes; avoid phrases like 'mentioned' or 'the context says'. "
    "Only touch on hobbies briefly and honestly, without overselling. "
    "Answer naturally and directly"
    "Do not speculate or invent details. Do not include citations or sources."
)

if "index" not in st.session_state:
    st.session_state.index = ingest(
        data_dir="./data",
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploader_seed" not in st.session_state:
    st.session_state.uploader_seed = 0

# active prompt selection
PROMPTS = {
    "PROMPT_INTERVIEW": PROMPT_INTERVIEW,
    "PROMPT_BRAG": PROMPT_BRAG,
    "PROMPT_STORY": PROMPT_STORY,
    "PROMPT_CONCISE": PROMPT_CONCISE,
}
if "active_prompt_key" not in st.session_state:
    st.session_state.active_prompt_key = "PROMPT_INTERVIEW"

st.title("Tristan Interview Agent")

with st.sidebar:
    st.subheader("Controls")
    temperature = st.slider("Creativity (temperature)", 0.0, 1.0, 0.15, 0.05)

    st.caption("Prompt preset")
    row1 = st.columns(2)
    if row1[0].button("Interview", use_container_width=True):
        st.session_state.active_prompt_key = "PROMPT_INTERVIEW"
    if row1[1].button("Brag", use_container_width=True):
        st.session_state.active_prompt_key = "PROMPT_BRAG"

    row2 = st.columns(2)
    if row2[0].button("Storyteller", use_container_width=True):
        st.session_state.active_prompt_key = "PROMPT_STORY"
    if row2[1].button("Concise", use_container_width=True):
        st.session_state.active_prompt_key = "PROMPT_CONCISE"

    st.write(f"Active: **{st.session_state.active_prompt_key}**")

    md_file = st.file_uploader(
        "Upload Markdown (.md)",
        type=["md"],
        key=f"md_uploader_{st.session_state.uploader_seed}"
    )
    if md_file is not None:
        try:
            raw_markdown = md_file.read().decode("utf-8", errors="ignore")
            updated = upsert_markdown(
                index=st.session_state.index,
                raw_markdown=raw_markdown,
                source=md_file.name,
                chunk_size=CHUNK_SIZE,
                chunk_overlap=CHUNK_OVERLAP
            )
            if updated is not None:
                st.session_state.index = updated
            st.toast("Vector base updated.")
        except Exception as e:
            st.error(f"Upload failed: {e}")
        finally:
            st.session_state.uploader_seed += 1
            st.rerun()

    if st.button("Rebuild index", use_container_width=True):
        st.session_state.index = ingest(
            data_dir="./data",
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        st.session_state.uploader_seed += 1
        st.success("Index rebuilt in memory.")
        st.rerun()

    if st.button("Reset chat history", use_container_width=True):
        st.session_state.messages = []
        st.success("Chat history cleared.")

if not OPENAI_KEY:
    st.warning("Missing OPENAI_API_KEY in secrets.")
client = OpenAI(api_key=OPENAI_KEY)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask an interview question about Tristan…")

def build_context(q: str):
    results = search(
        index=st.session_state.index,
        query=q,
        k=K,
        fetch_k=FETCH_K
    )
    docs = []
    for item in results:
        doc = item[0] if isinstance(item, tuple) else item
        page = getattr(doc, "page_content", None)
        if isinstance(page, str):
            docs.append(page)
    return "\n\n".join(docs)

def chat_completion(messages):
    resp = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=temperature,
    )
    return resp.choices[0].message.content

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    context = build_context(user_input)
    active_prompt = PROMPTS.get(st.session_state.active_prompt_key, "")

    llm_messages = []
    llm_messages.append({"role": "system", "content": active_prompt})
    llm_messages.append({"role": "system", "content": f"Context:\n{context}"})
    for m in st.session_state.messages:
        if m["role"] in ("user", "assistant"):
            llm_messages.append(m)

    with st.chat_message("assistant"):
        if client is None:
            st.error("OpenAI client not initialised.")
        else:
            reply = chat_completion(llm_messages)
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})