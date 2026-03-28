import streamlit as st
import requests
import json
import time

LOCAL_IP = "127.0.0.1"
EC2_IP = "100.48.95.121"


API_URL = f"http://{EC2_IP}:8000/build/stream"
DOWNLOAD_URL = f"http://{EC2_IP}:8000/download"
project_name_holder = {"name": None}



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

                            if "project_name" in data:
                                project_name_holder["name"] = data["project_name"]

                            if node == "planner":
                                planner_placeholder.info("Planner: Creating project structure...")

                            elif node == "architect":
                                architect_placeholder.success("Architect: Mapping file requirements...")

                            elif node == "coder":
                                coder_placeholder.write("Coder: Writing files...")

                            time.sleep(0.05)

                status.update(label="Build Finished!", state="complete", expanded=False)

            except Exception as e:
                st.error(f"Error: {e}")

    
    with col2:
        st.subheader("Project Status")
        st.success("Your project has been generated.")

        try:
            if project_name_holder["name"]:

                download_url = f"{DOWNLOAD_URL}?project_name={project_name_holder['name']}"

                download = requests.get(download_url)

                st.download_button(
                    label="⬇️ Download Project ZIP",
                    data=download.content,
                    file_name=project_name_holder["name"] + ".zip",
                    mime="application/zip"
                )

        except:
            st.error("Download failed")

        st.balloons()
