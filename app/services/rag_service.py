# app/services/rag_service.py

import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain.prompts import PromptTemplate

# role-based department filtering (same as before)
role_department_map = {
    "finance": "finance",
    "marketing": "marketing",
    "engineering": "engineering",
    "hr": "hr",
    "employee": "general",
    "c_level": None  # full access
}

class RagService:

    def __init__(self, persist_dir: str = "vector_store"):
        self.persist_dir = persist_dir

        self.embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vector_store = FAISS.load_local(
    self.persist_dir,
    embeddings=self.embedding,
    allow_dangerous_deserialization=True
)


        # Load local LLM model (small for now)
        self.model_name = "microsoft/phi-2"  # Or replace with "mistralai/Mistral-7B-Instruct-v0.1"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name, device_map="auto")

        self.generator = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)

        self.prompt_template = PromptTemplate(
            template="""
You are an assistant for FinSolve Technologies.
Use the following context to answer the user's question.

Context:
{context}

Question:
{question}

Answer:
""",
            input_variables=["context", "question"]
        )

    def get_relevant_documents(self, query: str, role: str):
        if role_department_map[role] is None:
            return self.vector_store.similarity_search(query, k=5)
        else:
            department = role_department_map[role]
            return self.vector_store.similarity_search(query, k=5, filter={"department": department})

    def ask(self, query: str, role: str) -> str:
        documents = self.get_relevant_documents(query, role)
        context = "\n".join([doc.page_content for doc in documents])

        full_prompt = self.prompt_template.format(context=context, question=query)
        response = self.generator(full_prompt, max_new_tokens=200)[0]['generated_text']
        return response
