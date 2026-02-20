import streamlit as st
import requests
import json
import time

API_URL = "http://127.0.0.1:8000/build/stream"

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="CodeTablet AI",
    page_icon="💻",
    layout="wide"
)

st.title("🤖 CodeTablet Engineer")
st.markdown("---")

user_prompt = st.text_area(
    "Project Description",
    placeholder="e.g., Create a Todo list app with local storage using HTML and JS",
    help="Describe the application you want the agent to build."
)


if st.button("Build Project", type="primary") and user_prompt:

    payload = {
        "user_prompt": user_prompt,
        "recursion_limit": 100
    }

    col1, col2 = st.columns([1, 1])

    #Execution Trace
    with col1:
        st.subheader("Execution Trace")

        planner_placeholder = st.empty()
        architect_placeholder = st.empty()
        coder_placeholder = st.empty()

        with st.status("Agent starting...", expanded=True) as status:

            try:
                response = requests.post(API_URL, json=payload, stream=True)

                for line in response.iter_lines():

                    if line:
                        decoded = line.decode("utf-8")

                        if decoded.startswith("data: "):

                            data = json.loads(decoded[6:])
                            node = data.get("node")

                            if node == "planner":
                                planner_placeholder.info("📝 Planner: Creating project structure...")

                            elif node == "architect":
                                architect_placeholder.success("🏗️ Architect: Mapping file requirements...")

                            elif node == "coder":
                                coder_placeholder.write("🛠️ Coder: Writing files...")

                            time.sleep(0.05)

                status.update(label="Build Finished!", state="complete", expanded=False)

            except Exception as e:
                st.error(f"Error: {e}")

    
    with col2:
        st.subheader("Project Status")
        st.success("Your project has been generated in the `generated_project` directory.")
        st.balloons()
