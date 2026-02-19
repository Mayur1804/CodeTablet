#from agent.tools import read_file
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.constants import END
from langgraph.graph import StateGraph
#from langgraph.prebuilt import create_react_agent
from langchain.agents import create_agent
from pydantic import BaseModel,Field

from agent.prompts import planner_prompt, architect_prompt, coder_system_prompt
from agent.states import Plan, ImplementationTask, TaskPlan, CoderState
from agent.tools import *

load_dotenv()

llm = ChatOpenAI(model= "gpt-4o")

def planner_agent(state: dict) -> dict:
    user_prompt = state["user_prompt"]
    response = llm.with_structured_output(Plan).invoke(planner_prompt(user_prompt))
    if response is None:
        raise ValueError("Failed to generate a plan -- Planner agent")
    print("planner agent response",response)
    return {"plan": response}

def architect_agent(state: dict) -> dict:
    plan: Plan = state["plan"]
    response = llm.with_structured_output(TaskPlan).invoke(architect_prompt(plan))
    if response is None:
        raise ValueError("Failed to generate a task plan -- Architect agent")
    # To maintain context of plan in the state I'm adding plan object in pydantic of Taskplan
    response.plan = plan
    print("architect agent response",response)
    return {"task_plan": response}

def coder_agent(state: dict) -> dict:
    coder_state = state.get("coder_state")
    if coder_state is None:
        coder_state = CoderState(task_plan=state['task_plan'],current_step_idx=0)
    
    steps = coder_state.task_plan.implementation_steps
    if coder_state.current_step_idx >= len(steps):
        return {"coder_state": coder_state, "status": "DONE"}
    
    current_task = steps[coder_state.current_step_idx]

    # Read 
    existing_content = read_file.run(current_task.filepath)

    user_prompt = (
        f"Task: {current_task.task_description}\n"
        f"File: {current_task.filepath}\n"
        f"Existing content:\n{existing_content}\n"
        "Use write_file(path, content) to save your changes."
        )
    system_prompt = coder_system_prompt()
    
    coder_tools = [read_file,write_file,list_files,get_current_directory]

    react_agent = create_agent(
        model=llm,
        tools=coder_tools
    )

    react_agent.invoke({"messages": [{"role":"system", "content": system_prompt},
                                                {"role": "user", "content": user_prompt}]})

    coder_state.current_step_idx += 1

    return {"coder_state": coder_state}
    

graph = StateGraph(dict)
graph.add_node("planner", planner_agent)
graph.add_node("architect", architect_agent)
graph.add_node("coder", coder_agent)
graph.add_edge("planner", "architect")
graph.add_edge("architect", "coder")
graph.add_conditional_edges(
    "coder",
    lambda s: "END" if s.get("status") == "DONE" else "coder",
    {"END": END, "coder": "coder"}
)


graph.set_entry_point("planner")

agent = graph.compile()


if __name__ == "__main__":
    user_prompt = "Build a very simple to-do application with HTML,CSS,JS with good graphics and UI "
    result = agent.invoke({"user_prompt": user_prompt})

    print(result)