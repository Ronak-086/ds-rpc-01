# app/services/ingestion_service.py
# app/services/ingestion_service.py

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma


import os
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.document_loaders import DirectoryLoader, TextLoader
# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.vectorstores import Chroma
from app.utils.config import OPENAI_API_KEY

class IngestionService:

    def __init__(self, data_dir: str = "resources/data", persist_dir: str = "vector_store"):
        self.data_dir = data_dir
        self.persist_dir = persist_dir

    def load_documents(self) -> List:
        all_documents = []

        # Loop over each department folder
        for department in os.listdir(self.data_dir):
            department_path = os.path.join(self.data_dir, department)

            # Load only .txt files for simplicity (can extend later)
            loader = DirectoryLoader(department_path, glob="*.txt", loader_cls=TextLoader)
            docs = loader.load()

            # Add department metadata to each document
            for doc in docs:
                doc.metadata["department"] = department
            all_documents.extend(docs)

        return all_documents

    def split_documents(self, documents: List) -> List:
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(documents)
        return chunks

    def embed_and_store(self, chunks: List):
        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        vectordb = Chroma.from_documents(chunks, embedding=embeddings, persist_directory=self.persist_dir)
        vectordb.persist()
        print("✅ Embeddings created and stored successfully.")

    def run_ingestion(self):
        print("🔎 Loading documents...")
        docs = self.load_documents()
        print(f"Loaded {len(docs)} documents")

        print("🔧 Splitting documents...")
        chunks = self.split_documents(docs)
        print(f"Created {len(chunks)} chunks")

        print("🧠 Generating embeddings...")
        self.embed_and_store(chunks)

