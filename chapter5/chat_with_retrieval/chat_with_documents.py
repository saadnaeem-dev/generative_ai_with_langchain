"""Chat with retrieval and embeddings.

Start ollama like this:
> OLLAMA_MODELS=/usr/share/ollama/.ollama/models OLLAMA_HOST=127.0.0.1:9999 ollama serve

See here for more help on ollama:
https://github.com/ollama/ollama/blob/main/docs/faq.md#where-are-models-stored
"""
import os
import tempfile

from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.checkpoint.memory import MemorySaver

from config import set_environment

from langchain_ollama.chat_models import ChatOllama
from langchain_ollama.embeddings import OllamaEmbeddings

from langchain_text_splitters import RecursiveCharacterTextSplitter

from chapter5.chat_with_retrieval.utils import LOGGER, load_document

set_environment()

LOGGER.info("setup LLM")
# Setup LLM and QA chain; set temperature low to keep hallucinations in check
LLM = ChatOpenAI(model="gpt-4o-mini", temperature=0.2, streaming=True)
# LLM = ChatOllama(
#     base_url="172.19.48.1:9997",
#     model="deepseek-r1:8b",
#     temperature=0.8,
#     num_predict=-1,
# )
LOGGER.info("configure_retriever")
# Create embeddings and store in vectordb:
# EMBEDDINGS = OllamaEmbeddings(
#     base_url="172.19.48.1:9997",
#     model="deepseek-r1:8b",
# )
EMBEDDINGS = OpenAIEmbeddings(
    model="text-embedding-3-large",
)
MEMORY = MemorySaver()
VECTOR_STORE = InMemoryVectorStore(embedding=EMBEDDINGS)

template = '''Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}'''

prompt = PromptTemplate.from_template(template)


@tool(response_format="content_and_artifact")
def retrieve(query: str):
    """Retrieve information related to a query."""
    retrieved_docs = VECTOR_STORE.similarity_search(query, k=2)
    serialized = "\n\n".join(
        f"Source: {doc.metadata}\n" f"Content: {doc.page_content}"
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs


def answer_question(input_message: str):
    return AGENT_EXECUTOR.invoke({"input": input_message})


def add_uploaded_docs(uploaded_files):
    docs = []
    temp_dir = tempfile.TemporaryDirectory()
    for file in uploaded_files:
        temp_filepath = os.path.join(temp_dir.name, file.name)
        with open(temp_filepath, "wb") as f:
            f.write(file.getvalue())
            docs.extend(load_document(temp_filepath))

    # Split each document documents:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # alternatively: HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    # Create vectordb with single call to embedding model for texts:
    VECTOR_STORE.add_documents(splits)


AGENT_EXECUTOR = AgentExecutor.from_agent_and_tools(
    create_react_agent(llm=LLM, tools=[retrieve], prompt=prompt),
    tools=[retrieve], handle_parsing_errors=False
)
