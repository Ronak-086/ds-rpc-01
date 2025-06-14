import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv("BACKEND_URL", "http://localhost:8000/chat")

st.title("FinSolve AI Assistant 🤖")

query = st.text_input("Enter your question")
role = st.selectbox("Select your role", ["engineering", "finance", "marketing", "hr", "employee", "c_level"])

if st.button("Ask"):
    if query:
        response = requests.post(
            backend_url,
            data={"message": query, "role": role}
        )
        if response.status_code == 200:
            st.write("Answer:")
            st.write(response.json()["response"])
        else:
            st.error("Something went wrong!")
