import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

class IngestionService:
    def __init__(self, data_dir="resources/data", persist_dir="vector_store"):
        self.data_dir = data_dir
        self.persist_dir = persist_dir
        self.embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    def load_documents(self):
        all_docs = []
        for department in os.listdir(self.data_dir):
            department_path = os.path.join(self.data_dir, department)
            loader = DirectoryLoader(department_path, glob="*.md", loader_cls=TextLoader)
            docs = loader.load()
            for doc in docs:
                doc.metadata["department"] = department
            all_docs.extend(docs)
        return all_docs

    def split_documents(self, docs):
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        return splitter.split_documents(docs)

    def embed_and_store(self, chunks):
        vectordb = FAISS.from_documents(chunks, embedding=self.embedding)
        vectordb.save_local(self.persist_dir)

    def run_ingestion(self):
        docs = self.load_documents()
        chunks = self.split_documents(docs)
        self.embed_and_store(chunks)
        print("✅ Ingestion complete!")
