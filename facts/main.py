from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
from typing import List
import requests

load_dotenv()


class LLMSCustomEmbeddings(Embeddings):
    def __init__(
        self,
        endpoint_url: str = "http://10.2.0.2:3333/v1/embeddings",
        model: str = "text-embedding-bge-base-en-v1.5"
    ):
        self.endpoint_url = endpoint_url
        self.model = model

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        payload = {
            "model": self.model,
            "input": texts
        }
        response = requests.post(self.endpoint_url, json=payload)
        response.raise_for_status()
        # Return embeddings for all documents
        return [item["embedding"] for item in response.json()["data"]]

    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text])[0]


def create_embeddings(mode: str = "local") -> Embeddings:
    """Create embeddings based on the specified mode."""
    if mode == "local":
        return LLMSCustomEmbeddings()
    elif mode == "remote":
        return OpenAIEmbeddings()
    else:
        raise ValueError("Invalid mode. Choose 'local' or 'remote'.")


def setup_chroma_db():
    """Setup Chroma DB with the specified embeddings."""
    embeddings = create_embeddings(mode="local")

    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=200,
        chunk_overlap=0
    )

    loader = TextLoader("facts.txt")
    docs = loader.load_and_split(
        text_splitter=text_splitter
    )
    db = Chroma.from_documents(
        docs,
        embedding=embeddings,
        persist_directory="emb"
    )
    return db


db = setup_chroma_db()


def search_facts(query: str):
    """Search for facts in the Chroma DB."""
    results = db.similarity_search(query)
    for result in results:
        print("\n")
        print(result.page_content)


if __name__ == "__main__":
    search_facts("What is an interesting fact about the English language?")
