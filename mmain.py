import streamlit as st
import time
from agent.graph import agent

# Basic Page Configuration
st.set_page_config(page_title="CodeTablet AI", page_icon="💻", layout="wide")

## --- UI Header ---
st.title("🤖 CodeTablet Engineer (Local)")
st.markdown("---")

## --- Sidebar Configuration ---
with st.sidebar:
    st.header("Settings")
    recursion_limit = st.slider("Step Limit", 10, 200, 100)
    if st.button("Clear Terminal"):
        st.rerun()

## --- Main Interface ---
user_prompt = st.text_area(
    "Project Description",
    placeholder="e.g., Create a Todo list app with local storage using HTML and JS",
    help="Describe the application you want the agent to build."
)

if st.button("Build Project", type="primary") and user_prompt:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Execution Trace")
        with st.status("Agent starting...", expanded=True) as status:
            for event in agent.stream(
                {"user_prompt": user_prompt},
                {"recursion_limit": recursion_limit}
            ):
                for node_name, output in event.items():
                    if node_name == "planner":
                        st.write("📝 **Planner:** Creating project structure...")
                        if isinstance(output, dict) and output.get('plan'):
                            st.info(f"Plan: {getattr(output['plan'], 'description', 'generated')}")
                    elif node_name == "architect":
                        st.write("🏗️ **Architect:** Mapping out file requirements...")
                        if isinstance(output, dict) and output.get('task_plan'):
                            steps = getattr(output['task_plan'], 'implementation_steps', [])
                            st.success(f"Generated {len(steps)} implementation tasks.")
                    elif node_name == "coder":
                        if isinstance(output, dict) and output.get('coder_state'):
                            curr_idx = getattr(output['coder_state'], 'current_step_idx', 0)
                            total = len(getattr(output['coder_state'].task_plan, 'implementation_steps', []))
                            st.write(f"🛠️ **Coder:** Writing file {curr_idx}/{total}...")
                time.sleep(0.1)
            status.update(label="Build Finished!", state="complete", expanded=False)

    with col2:
        st.subheader("Project Status")
        st.success("Your project has been generated in the `generated_project` directory.")
        st.balloons()
