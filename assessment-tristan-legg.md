# Candidate Assessment – Tristan Legg

**Repository:** [https://github.com/TristanJLegg/TristanInterviewAgent](https://github.com/TristanJLegg/TristanInterviewAgent)

## Rubric Evaluation

| Category | Score (0–5) | Observations |
|----------|-------------|--------------|
| **Context Handling** | **4** | Builds context by retrieving relevant Markdown chunks with FAISS before each response【F:app.py†L190-L203】 |
| **Agentic Thinking** | **4** | Sidebar prompt presets toggle interview, brag, story and concise tones, changing system prompt and verbosity【F:app.py†L123-L138】 |
| **Use of Personal Data** | **4** | Dataset combines CV, Q&A, project summaries and values in Markdown files【F:README.md†L25-L33】【e3310e†L1-L2】 |
| **Build Quality** | **3** | Streamlit app runs, but includes duplicate prompt mappings and a non-returning `upsert_markdown` that is treated as if it returns a value【F:app.py†L76-L88】【F:app.py†L150-L158】【F:vectorstore.py†L84-L115】 |
| **Voice & Reflection** | **4** | System prompts enforce first-person UK-English answers and discourage invented details, keeping responses in Tristan’s voice【F:app.py†L17-L29】 |
| **Bonus Effort** | **4** | Upload feature, index rebuild, and chat reset add useful polish beyond base requirements【F:app.py†L142-L174】 |
| **AI Build Artifacts** | **4** | README links to ChatGPT conversations for data creation and coding, showing AI-assisted workflow【F:README.md†L96-L128】 |
| **RAG Usage (Optional)** | **4** | Uses in-memory FAISS with max-marginal-relevance search to diversify retrieved context【F:app.py†L190-L203】【F:vectorstore.py†L117-L125】 |
| **Submission Completeness** | **5** | GitHub repo, deployed Streamlit app, and video walkthrough provided in submission email【F:email-tristan-legg.md†L1-L5】 |

**Total Score:** **36 / 45**

## Critical Feedback & Suggestions

- **Duplicate prompt dictionary** – The `PROMPTS` mapping is defined twice, risking future inconsistencies【F:app.py†L76-L88】. *Remove the first definition or consolidate into one dictionary.*
- **`upsert_markdown` return mismatch** – `upsert_markdown` mutates the FAISS index but returns nothing, yet the caller checks for a returned value before updating state【F:app.py†L150-L158】【F:vectorstore.py†L84-L115】. *Return the updated index or drop the conditional reassignment.*
- **Unused imports** – `List`, `Tuple`, and `Union` are imported but unused, adding noise to the codebase【F:app.py†L4】. *Remove unused imports to improve readability and linting results.*
- **Missing tests and error handling** – No automated tests or validation of retriever results are provided. *Add unit tests for `vectorstore.py` and checks for empty retrievals to increase reliability.*

---

Prepared for internal review by the CTO panel.
