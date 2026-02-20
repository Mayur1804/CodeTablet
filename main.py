import streamlit as st
import requests
import time

API_URL = "http://127.0.0.1:8000/build"

st.set_page_config(page_title="CodeTablet AI", page_icon="💻", layout="wide")

st.title("🤖 CodeTablet Engineer")
st.markdown("---")

with st.sidebar:
    st.header("Settings")
    recursion_limit = st.slider("Step Limit", 10, 200, 100)

user_prompt = st.text_area("Project Description")

if st.button("Build Project") and user_prompt:

    payload = {
        "user_prompt": user_prompt,
        "recursion_limit": recursion_limit
    }

    response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        st.success("Project Generated Successfully 🚀")
        st.json(response.json())
    else:
        st.error("Something went wrong!")
