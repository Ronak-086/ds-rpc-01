# app/frontend/streamlit_app.py

import streamlit as st
import requests
from requests.auth import HTTPBasicAuth

st.set_page_config(page_title="FinSolve Chatbot", page_icon="🤖")

st.title("💼 FinSolve Internal Chatbot")

# Backend FastAPI URL (running in Codespaces)
backend_url = "http://localhost:8000/chat"

# User Login Section
st.sidebar.header("🔐 User Login")

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

# Chat Interface
if username and password:
    st.success(f"Logged in as: {username}")
    message = st.text_input("Enter your query:")

    if st.button("Ask"):
        with st.spinner("Generating response..."):

            response = requests.post(
                backend_url,
                auth=HTTPBasicAuth(username, password),
                data={"message": message}
            )

            if response.status_code == 200:
                output = response.json()["response"]
                st.write("### Response:")
                st.write(output)
            else:
                st.error("Error: Invalid Credentials or Backend Issue.")
else:
    st.warning("Please enter your credentials to proceed.")
