# app/services/ingestion_service.py

import os
import pickle
from typing import List
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

class IngestionService:

    def __init__(self, data_dir: str = "resources/data", persist_dir: str = "vector_store"):
        self.data_dir = data_dir
        self.persist_dir = persist_dir

        self.embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    def load_documents(self) -> List:
        all_documents = []

        for department in os.listdir(self.data_dir):
            department_path = os.path.join(self.data_dir, department)

            docs = []
            for ext in ["*.txt", "*.md"]:
                loader = DirectoryLoader(department_path, glob=ext, loader_cls=TextLoader)
                docs.extend(loader.load())

            for doc in docs:
                doc.metadata["department"] = department

            all_documents.extend(docs)

        return all_documents

    def split_documents(self, documents: List) -> List:
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(documents)
        return chunks

    def embed_and_store(self, chunks: List):
        vector_store = FAISS.from_documents(chunks, embedding=self.embedding)

        # Persist locally
        vector_store.save_local(self.persist_dir)
        print("✅ Embeddings stored in FAISS locally.")

    def run_ingestion(self):
        print("🔎 Loading documents...")
        docs = self.load_documents()
        print(f"Loaded {len(docs)} documents")

        print("🔧 Splitting documents...")
        chunks = self.split_documents(docs)
        print(f"Created {len(chunks)} chunks")

        print("🧠 Generating embeddings...")
        self.embed_and_store(chunks)
