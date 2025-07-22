# from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from redundant_filter_retriever import RedundantFilterRetriever
from dotenv import load_dotenv
import langchain
from main import create_embeddings
import os

langchain.debug = True

load_dotenv()


def get_model() -> ChatOpenAI:
    """Get the chat model based on the environment variable."""
    # Initialize the chat model
    mode = os.environ.get("MODEL_MODE", "local")
    if mode == "local":
        llm = os.environ.get("LLM_MODEL_NAME")
        base_url = os.environ.get("LLM_BASE_URL")
        return ChatOpenAI(
            model_name=llm,
            openai_api_base=base_url,
            openai_api_key="",
        )
    elif mode == "remote":
        # API key in .env is mandatory
        return ChatOpenAI()
    else:
        raise ("MODEL_MODE environment variable should be local/remote")


chat = get_model()
embeddings = create_embeddings()
db = Chroma(
    persist_directory="emb",
    embedding_function=embeddings
)
retriever = RedundantFilterRetriever(
    embeddings=embeddings,
    chroma=db
)


# Function to format documents
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# Create prompt template
template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

# Create LCEL chain
chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | chat
    | StrOutputParser()
)

result = chain.invoke(
    "What is an interesting fact about the English language?"
)

print(result)
