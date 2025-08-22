# vectorstore.py
from __future__ import annotations

import os
import re
from pathlib import Path
from typing import List

from langchain.schema import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


_HEADER_SPLITTER = MarkdownHeaderTextSplitter(
    headers_to_split_on=[("#", "H1"), ("##", "H2"), ("###", "H3")]
)

_CLEAN_SECTION_PATTERN = re.compile(
    r"(?im)^[ \t]*#{1,6}[ \t]*"
    r"(license|licence|contributing|acknowledgements?|code of conduct)\b.*?"
    r"(?=^[ \t]*#{1,6}[ \t]*|\Z)",
    flags=re.DOTALL,
)

_CODE_FENCE_PATTERN = re.compile(r"```.*?```|~~~.*?~~~", flags=re.DOTALL)


def _clean_markdown(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = _CODE_FENCE_PATTERN.sub("", text)
    text = _CLEAN_SECTION_PATTERN.sub("", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _section_path(md_meta: dict) -> str:
    parts = [md_meta.get("H1", ""), md_meta.get("H2", ""), md_meta.get("H3", "")]
    return " / ".join([p for p in parts if p])


def ingest(
    data_dir: str,
    chunk_size: int,
    chunk_overlap: int
) -> FAISS:
    paths = sorted(Path(data_dir).rglob("*.md"))
    section_docs: List[Document] = []

    for p in paths:
        try:
            raw = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        cleaned = _clean_markdown(raw)
        if not cleaned:
            continue

        parts = _HEADER_SPLITTER.split_text(cleaned)
        if not parts:
            parts = [Document(page_content=cleaned, metadata={})]

        for d in parts:
            section = _section_path(d.metadata)
            section_docs.append(
                Document(
                    page_content=d.page_content.strip(),
                    metadata={"source": str(p), "section": section},
                )
            )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    chunks = splitter.split_documents(section_docs)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    index = FAISS.from_documents(chunks, embeddings, normalize_L2=True)
    return index


def upsert_markdown(
    index: FAISS,
    raw_markdown: str,
    source: str,
    chunk_size: int,
    chunk_overlap: int
) -> None:
    cleaned = _clean_markdown(raw_markdown)
    if not cleaned:
        return
    parts = _HEADER_SPLITTER.split_text(cleaned)
    if not parts:
        parts = [Document(page_content=cleaned, metadata={})]

    section_docs: List[Document] = []
    for d in parts:
        section = _section_path(d.metadata)
        section_docs.append(
            Document(
                page_content=d.page_content.strip(),
                metadata={"source": source, "section": section},
            )
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    chunks = splitter.split_documents(section_docs)
    index.add_documents(chunks)


def search(
    index: FAISS,
    query: str,
    k: int,
    fetch_k: int,
) -> List[Document]:
    fk = max(12, k * 3) if not fetch_k or fetch_k < k else fetch_k
    return index.max_marginal_relevance_search(query, k=k, fetch_k=fk)


def main():
    index = ingest("./data", chunk_size=1000, chunk_overlap=100)

    docs = search(index, query="What are your hobbies?", k=5, fetch_k=10)
    for d in docs:
        print(f"Source: {d.metadata.get('source')} [{d.metadata.get('section')}]")
        print(d.page_content[:200], "...\n")

    new_md = "# Hobbies\nI enjoy competitive gaming and 3D printing.\n\n## Details\nI use an Ender printer."
    upsert_markdown(index, new_md, source="in_memory/new_hobbies.md", chunk_size=1000, chunk_overlap=100)

    print("After upsert:\n")
    docs = search(index, query="What printer do you use?", k=3, fetch_k=0)
    for d in docs:
        print(f"Source: {d.metadata.get('source')} [{d.metadata.get('section')}]")
        print(d.page_content[:200], "...\n")


if __name__ == "__main__":
    main()