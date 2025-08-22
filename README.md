# Tristan Interview Agent

This is a RAG interview assistant built to emulate myself in interview settings. It combines a curated knowledge base of my CV, values, GitHub READMEs, and prepared answers with GPT-5-mini to ensure responses stay grounded, natural, and personalised.

**Website**: https://tristaninterviewagent.streamlit.app  

# Setup and Design

## Technology Stack

- **Streamlit**: lightweight, simple to use, and easy to deploy for building web apps.  
- **FAISS**: fast in-memory vector search that avoids database dependencies, making it ideal to use with deployed Streamlit apps.  
- **OpenAI text-embedding-3-large**: high-quality embeddings that improve retrieval accuracy. Quality was prioritised over cost as the system does not need to scale quickly.  
- **GPT-5-mini**: default generation model, offering a good balance of speed and cost. The mini version is effective for directed tasks like this.  
- **LangChain**: provides utilities for cleaning, splitting, and loading documents.  

## Design Choices

- **RAG**: retrieval ensures answers stay grounded in accurate knowledge and avoids bloating each agent prompt.  
- **Prompts**: the agent is prompted to frame itself as me in an interview setting. It avoids citations, keeps answers grounded in RAG context, and uses session-based chat memory. These details were key to making the agent sound like me.  
- **Refusals**: strict refusal prompts made the agent reject too many questions it could actually answer from my data. Instead, it was prompted not to speculate or invent details. This improved accuracy while keeping answers useful, though on rare occasions the bot may still make something up.  
- **Max Marginal Relevance (MMR)**: used to increase diversity in retrieved chunks, reducing redundancy and surfacing more relevant aspects of an answer.  
- **Hyperparameters**: baseline values for chunk size (1000), overlap (150), and top-k retrieval (4) were taken from standard practice, then refined through experimentation. `fetch_k` was set to 12, giving the retriever a wider pool of candidate chunks before applying MMR.  

## Data

All data is stored in Markdown format for easy chunking and cleaning using headings.  

- **CV.md**: includes contact details, qualifications, experience, projects, and skills.  
- **Questions.md**: 35 answers to common interview questions (AI-generated questions, my own answers). Includes both work-related and personal questions to add more personality. This also gets the bot used to the question/answer format while giving it enough context to handle unseen questions.  
- **Project.md**: three short READMEs from my GitHub projects, giving examples of my writing style and project context.  
- **Values.md**: concise lists of my values and other personal details that the agent can integrate into responses.  

## Additional Features Implemented

- **Tone Switcher**: four chatbot tones that change the model output: normal interview mode, bragging, storytelling, and concise. These modes modify the system prompt and GPT-5 verbosity parameter, while still keeping answers truthful and aligned with my context.  
- **Extending Dataset**: upload feature for adding new Markdown files directly into the dataset.  
- **Rebuild Index**: resets the dataset to its original state, removing uploaded documents.  
- **Reset Chat History**: clears chat history for ease of use.  

## System Prompts

The base system prompt was written by me and refined to remove response issues. It was later adapted for different tones.

```python3
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
    "Simply answer naturally and directly, as if speaking in an interview. Try to keep answers short."
    "Do not speculate or invent details. Do not include citations or sources."
)
```

# Samples

## What is your engineering philosophy?

My engineering philosophy focuses on building and shipping AI that delivers value quickly, reliably, and responsibly.

- Results first: I set clear success metrics and prefer minimal solutions that achieve impact rather than unused perfection.  
- Iterative and experimental: models are hypotheses. I design controlled experiments, measure, learn, and iterate quickly.  
- Rigorous engineering: reproducible pipelines, modular code, tests, and monitoring ensure dependable systems in production.  
- Responsible and honest: integrity shapes my design choices. I include bias checks, explainability, and safety trade-offs.  
- Collaborative and compassionate: I communicate trade-offs clearly and work closely with teammates and stakeholders.  
- Continuous learning: I review failures, adjust processes, and update code so mistakes are not repeated.  

Discipline, integrity, and curiosity guide how I approach every project.  

## What motivates you to take on ambitious AI projects?

I am motivated by curiosity and technical challenge. I enjoy tackling hard problems, especially improving model accuracy and alignment, and turning research into reliable systems. I also value opportunities to lead teams, mentor others, and see work create real-world impact. Ambitious projects let me combine deep learning expertise, product thinking, and leadership to solve meaningful problems.  

## How do you approach teamwork when tackling complex technical challenges?

I start by aligning the team on a clear, measurable goal. I then break the problem into parallel parts (data, modelling, infrastructure, evaluation) so progress can happen simultaneously. I encourage rapid prototyping and small experiments with clear experiment tracking to ensure results are reproducible.  

Daily syncs or short pairing sessions keep everyone coordinated. Code reviews and shared notebooks spread understanding and support teammates. When roadblocks arise, I use structured troubleshooting: form hypotheses, run targeted tests, and iterate on promising fixes.  

After delivery, we hold a retrospective to capture what went wrong and update processes or tooling to prevent repeat mistakes. Overall, I value collaboration, adaptability, and continuous learning so the team improves together.  

# Future Improvements

The main improvement I want to make is increasing response accuracy. The bot occasionally invents details or projects, especially when asked about topics far outside its dataset. This is most noticeable in storytelling mode, which tends to produce long, romanticised answers. Ideally, in such cases, the bot should refuse and suggest contacting me directly instead.  

I would also like to include more data about me and my personal experiences, so the agent’s responses sound even closer to how I would answer.  

# Show My Thinking

This project was built under a short time frame, with encouragement to work AI-natively. I used AI for large parts of the development process, choosing ChatGPT-5 because it can one-shot problems better than earlier models and makes conversations easy to share.  

## Data Creation

I used an AI agent to generate 35 interview questions covering technical, non-technical, and personal topics. I then wrote all the answers myself, ensuring the dataset was fully based on my own words and experiences. This gave the bot both structured examples and enough context to handle unseen questions.  

Link to the conversation: https://chatgpt.com/share/68a82acc-779c-8013-91d0-cc024c1618b3

## Vector Database

I built the ingestion, search, and upsert features (`vectorstore.py`) with the help of GPT-5.  

I gave it a detailed prompt specifying the embedding model, database library, function interfaces, and utilities for cleaning, chunking, and MMR-based retrieval. With experimentation, this created a working implementation.  

I then edited the code myself to simplify logic, fix type issues, and align it with the external library requirements. I also added an `upsert_markdown` function with an AI draft as a base, integrating it into the codebase.  

Link to the conversation: https://chatgpt.com/share/68a79960-ee0c-8013-b328-f2ef5fb851b5

## The Streamlit App

I developed most of the frontend (`app.py`) with GPT-5 assistance.  

I prompted it to build a Streamlit app that emulates me in interviews, uses `vectorstore.py` for ingestion, search, and upsert, maintains chat history in `st.session_state`, and builds system messages with retrieved context. I also requested sidebar controls for index rebuilding, chat resets, and Markdown uploads.  

The AI produced a functional app, which I refined by fixing type issues, adapting it from GPT-4’s `temperature` to GPT-5’s `verbosity`, and adding preset prompt styles (Interview, Brag, Story, Concise). I selected baseline retrieval parameters and tested configurations to optimise performance. I also wrote and refined the system prompts to ensure each style gave the intended tone and depth.  

The result is a simple but flexible interface connecting the vector store and model into an interactive interview agent.  

Link to the conversation: https://chatgpt.com/share/68a82fdf-5864-8013-bbca-29c5f0be31bd

## Breakdown of AI vs Manual Work  

**AI-generated**  
- Initial `vectorstore.py` (ingestion, search, chunking, MMR).  
- First draft of `app.py` including chat interface, sidebar controls, and Markdown upload feature.  
- Prompt style switcher (Interview, Brag, Story, Concise) and base layout.  

**Manually edited**  
- Fixed type and SDK issues with external libraries.  
- Selected and tuned baseline parameters (`chunk_size`, `chunk_overlap`, `k`, `fetch_k`).  
- Authored and refined all system prompts.  
- Made all design, model, and architecture choices.  
- Wrote the detailed descriptions and interfaces used to guide the AI agents.  
- Ensured the app remained minimal and fully in-memory.  

**AI-assisted, refined by me**  
- `upsert_markdown` function drafted by AI and integrated by me.  
- Migrated from GPT-4’s `temperature` to GPT-5’s `verbosity`, resolving type issues.  
- Streamlit uploader fix (`uploader_seed` + rerun) suggested by AI and applied by me.  
