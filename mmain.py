import streamlit as st
import time
from agent.graph import agent

# Basic Page Configuration
st.set_page_config(page_title="CodeTablet AI", page_icon="💻", layout="wide")

## --- UI Header ---
st.title("🤖 CodeTablet Engineer")
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
    # Create a layout with two columns: Progress and Output
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Execution Trace")
        # The status container groups all agent actions
        with st.status("Agent starting...", expanded=True) as status:
            
            # Using .stream() to catch every node transition
            for event in agent.stream(
                {"user_prompt": user_prompt},
                {"recursion_limit": recursion_limit}
            ):
                for node_name, output in event.items():
                    # Visual feedback for each agent node
                    if node_name == "planner":
                        st.write("📝 **Planner:** Creating project structure...")
                        st.info(f"Plan: {output['plan'].description}")
                        
                    elif node_name == "architect":
                        st.write("🏗️ **Architect:** Mapping out file requirements...")
                        steps = output['task_plan'].implementation_steps
                        st.success(f"Generated {len(steps)} implementation tasks.")
                        
                    elif node_name == "coder":
                        if "coder_state" in output:
                            curr_idx = output['coder_state'].current_step_idx
                            total = len(output['coder_state'].task_plan.implementation_steps)
                            st.write(f"🛠️ **Coder:** Writing file {curr_idx}/{total}...")
                            
                # Optional: slight delay to make the UI feel smoother
                time.sleep(0.1)
            
            status.update(label="Build Finished!", state="complete", expanded=False)

    with col2:
        st.subheader("Project Status")
        st.success("Your project has been generated in the `generated_project` directory.")
        st.balloons()