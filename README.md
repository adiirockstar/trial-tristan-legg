# Tristan Interview Agent

This is an RAG interview assistant built to emulate myself in interview settings. It combines a curated knowledge base of my CV, values, GitHub READMEs and prepared answers with GPT-5-mini to ensureresponses stay grounded, natural, and personalised.

## Links

- **GitHub**: https://github.com/TristanJLegg/TristanInterviewAgent
- **Website**: https://tristaninterviewagent.streamlit.app

# Setup and Design

## Technology Stack

- **Streamlit**: lightweight, easy to use, easy to install web application library which is easy to deploy.
- **FAISS**: fast in-memory vector search that avoids database dependancies making it useful to utilise alongside deployed Streamlit apps.
- **OpenAI text-embedding-3-large**: high-quality embeddings and retrieval accuracy. Quality was prioritised over cost as this system will likely not need to scale rapidly.
- **GPT-5-mini**: default generation model used, good balance of speed and cost with the mini version being effective at directed tasks like this.
- **LangChain**: provides tools for cleaning, splitting and loading documents.

## Design Choices

- **RAG**: retrieval helps answers be grounded in accurate knowledge and avoids bloating each prompt to the agent.
- **Prompts**: Prompted the agent to frame themselves as me in an interview setting, avoid citations, try to keep answers grounded in their RAG context and session based chat memory. These details were all important in making the agent respond like me.
- **Refusals**: Attempts at prompt the GPT chatbot to outright refuse to comment whenever it was not sure caused the agent to refuse too many questions that it could work out from my data. The decision was made to instead prompt it to not speculate and invent details. This was a good mix of effectiveness and accuracy for the bot but occasionally the bot may make up something.
- **Max Marginal Relevance**: MMR retrieval was used to increase the diversity of retrieved chunks, reducing redundancy and improving the likelihood of surfacing all relevant aspects of an answer.
- **Hyperparameters**: Baseline values for chunk size (1000), overlap (150), and top-k retrieval (4) were adopted from standard practice, then refined through experimentation. Additionally, fetch_k (12) was set higher than k so the retriever has a wider pool of candidate chunks to choose from before applying MMR, improving the quality and diversity of the result.

## Data

All data is given in markdown format to easily chunk and clean the data using markdown headings.

- **CV.md**: gives the both context to my background, contact-details, qualifications, experience, projects and skills.
- **Questions.md**: Answers to 35 different common interview questions (questions AI generated and answered by me), with a mix of both work and non related questions to give the chatbot more of my character and personality. The decision was made to include this file as it both gets the bot used to the question and answer format it will be used in but gives it enough context about me (as interview questions tend to be quite encompassing) to be able to answer questions not in its dataset.
- **Project.md**: 3 Different simple READMEs done for my GitHub projects to give some examples of my writing while giving the bot more context on my project.
- **Values.md**: Very short and punchy lists of details about my values as well as other things about me that the agent can easily integrate into responses.

## Additional Features Implemented
- **Tone Switcher**: Implemented 4 different chatbot tones that affect model output including the normal interview mode, bragging, storytelling and concise. These modes change the system prompt to modify the way the chatbot will respond why all still trying to emulate myself and keep its responses rooted in the truthful context I have provided it. The modes also change the GPT-5 verbosity parameter that controls the response length and detail.
- **Extending Dataset**: Included a upload feature to the app that will accept markdown files and upsert them into the dataset, giving the chatbot additional knowledge.
- **Rebuild Index**: Rebuilds the dataset back to the original, removing all uploaded documents.
- **Reset Chat History**: Quickly resets the chat for ease-of-use.

## System Prompts

The system prompt was written by me and edited to remove issues with its responses.

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
    "Simply answer naturally and directly, as if speaking in an interview."
    "Do not speculate or invent details. Do not include citations or sources."
)
```

This is the original system prompt that later got modified for different tones.

# Samples

# Future Improvements

The main thing I would like to work on in the future is the accuracy of the responses produced by the chatbot. The bot will occassionally invent details or projects that I worked on when it gets asked a question that is very different to anything in its dataset. This is more apparent when using the Storytelling narrative tone mode which clearly wants to each response to be long and romanticised. Ideally I would like the bot in these settings to refuse to answer and request you send me an email to get a response.

Additionally I would like to add and incorporate more interesting data about me and my personality so that the agent can respond more akin to me given my own personal experiences. 

# Show my Thinking

Due to the short time-frame of this project and the encouragement to work AI-natively, I attempted to use AI large parts of this project. I specifically chose to use ChatGPT-5 conversations so that I could easily share them here with you and because of the improved ability of GPT-5 to be able to one-shot problems compared to other models.

## Data Creation

I sped up the data creation process by utilising an agent to provide 35 different common interview questions about my technical skills, non-technical skills and non-work related details. This was to give a good mix of answers that would get the agent used to the interview structure and give the agent enough context about me to let it infer knowledge when asked a question not directly in its dataset. I personally wrote the answer to each question as it is crucial that is completely based off of me and my responses as that is what the chatbot is trying to emulate.

Link to the conversation: https://chatgpt.com/share/68a82acc-779c-8013-91d0-cc024c1618b3

## Vector Database

I wrote the ingestion, search and upsert features of the application (vectorstore.py) using a GPT-5 chat agent. 

I gave it a detailed prompt defining the code description, embedding model, vector database library, function interfaces, dataset cleaning, chunking, max marginal relevance utility and function descriptions for RAG ingestion and search. With some experimentation this successfully created a working `vectorstore.py` file. 

After incorporating some edits written by me, simplifying the code as well fixing errors due to the type requirements of the external libraries, I asked it to implement (with my edited code) an upsert markdown function that takes raw text inputs and adds it to our vector database.

Link to the conversation: https://chatgpt.com/share/68a82acc-779c-8013-91d0-cc024c1618b3

## The Streamlit App

I built the majority of the Streamlit frontend (app.py) and chat functionality with a GPT-5 chat agent.

I prompted it with detailed requirements: the app should emulate me in an interview, use my existing vectorstore.py (ingest, search, upsert_markdown), maintain chat history in st.session_state, build context from top-k retrieved chunks, and pass this as a system message before each user input. I also asked for sidebar controls for rebuilding the index, resetting the conversation, and uploading Markdown files to update the vector base. I told it what libraries it could use to maintain consistency between agent code.

With some experimentation this produced a working Streamlit app, which I refined by fixing errors — especially type issues with the external libraries — and by making edits where the generated code didn’t quite align with the SDK requirements. I also used GPT-5 to quickly adapt the app from GPT-4’s temperature parameter to GPT-5’s categorical verbosity, and to integrate multiple preset prompt styles (Interview, Brag, Story, Concise) each with default verbosity values.

Alongside these AI-assisted iterations, I manually selected baseline parameters such as chunk sizes, overlap, and retrieval settings (k and fetch_k), and tested different configurations to optimise performance. I also wrote and refined the system prompts for each style to ensure the chatbot’s answers matched the intended tone and depth.

The result is a minimal but flexible chat interface that ties the vector store and model together into an interactive interview agent.

Link to the conversation: https://chatgpt.com/share/68a82fdf-5864-8013-bbca-29c5f0be31bd