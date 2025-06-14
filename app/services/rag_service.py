import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

role_department_map = {
    "engineering": "engineering",
    "finance": "finance",
    "marketing": "marketing",
    "hr": "hr",
    "employee": "general",
    "c_level": None
}

class RagService:
    def __init__(self, persist_dir="vector_store"):
        self.embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vector_store = FAISS.load_local(persist_dir, embeddings=self.embedding, allow_dangerous_deserialization=True)

    def retrieve(self, query, role):
        docs = self.vector_store.similarity_search(query, k=5)
        if role_department_map[role] is None:
            return docs
        return [doc for doc in docs if doc.metadata.get("department") == role_department_map[role]]

    def generate_answer(self, context, query):
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        prompt = f"""
        You are a company assistant. Answer based only on this context:

        Context:
        {context}

        Question:
        {query}

        Answer:
        """
        response = model.generate_content(prompt)
        return response.text

    def ask(self, query, role):
        docs = self.retrieve(query, role)
        context = "\n".join([doc.page_content for doc in docs])
        return self.generate_answer(context, query)
