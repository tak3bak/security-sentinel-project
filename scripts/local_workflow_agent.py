from typing import Annotated, TypedDict
import operator
import subprocess

from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END

# 1. Define the Shared State Schema
class WorkflowState(TypedDict):
    messages: Annotated[list, operator.add]
    execution_step: str

# 2. Define Real Execution Tools
@tool
def execute_shell_command(command: str) -> str:
    """Executes a safe shell command on the local system and returns the output or error."""
    print(f"\n[Execution Tool] Running command: {command}")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=15
        )
        if result.returncode == 0:
            return f"Success:\n{result.stdout.strip()}"
        else:
            return f"Error (Exit code {result.returncode}):\n{result.stderr.strip()}"
    except Exception as e:
        return f"Execution failed: {str(e)}"

tools = [execute_shell_command]
tools_by_name = {tool.name: tool for tool in tools}

# Initialize local LLM via Ollama
llm = ChatOllama(model="llama3.2", temperature=0).bind_tools(tools)

# 3. Define Graph Nodes
def agent_reasoning_node(state: WorkflowState) -> dict:
    """Core reasoning node where the local model decides what execution steps to take."""
    print("\n--- [Node: Agent Reasoning] ---")
    system_prompt = SystemMessage(
        content=(
            "You are an active workflow execution agent. "
            "Your objective is to achieve the user's goal by proactively invoking execution tools "
            "to run commands, check environments, or manage tasks. Review the output and proceed until complete."
        )
    )
    response = llm.invoke([system_prompt] + state["messages"])
    return {"messages": [response], "execution_step": "evaluated"}

def tool_execution_node(state: WorkflowState) -> dict:
    """Executes the shell commands requested by the model."""
    print("\n--- [Node: Tool Execution Engine] ---")
    last_message = state["messages"][-1]
    
    outputs = []
    for tool_call in last_message.tool_calls:
        tool_fn = tools_by_name[tool_call["name"]]
        tool_output = tool_fn.invoke(tool_call["args"])
        outputs.append(
            ToolMessage(
                content=str(tool_output),
                tool_call_id=tool_call["id"]
            )
        )
        
    return {"messages": outputs, "execution_step": "executed_tools"}

# 4. Define Conditional Routing Logic
should_continue = lambda state: "continue" if state["messages"][-1].tool_calls else "end"

# 5. Build and Compile the Workflow Graph
workflow_builder = StateGraph(WorkflowState)

workflow_builder.add_node("agent_reasoning", agent_reasoning_node)
workflow_builder.add_node("tool_execution", tool_execution_node)

workflow_builder.add_edge(START, "agent_reasoning")
workflow_builder.add_conditional_edges(
    "agent_reasoning",
    should_continue,
    {
        "continue": "tool_execution",
        "end": END
    }
)
workflow_builder.add_edge("tool_execution", "agent_reasoning")

app = workflow_builder.compile()

# 6. Run the Execution Agent
if __name__ == "__main__":
    initial_input = {
        "messages": [HumanMessage(content="Check what docker containers are currently running on this system.")],
        "execution_step": "initialized"
    }
    
    print("Starting Workflow Execution Agent (Free / Local)...")
    
    final_state = app.invoke(initial_input)
    print("\n=== Final Agent Output ===")
    print(final_state["messages"][-1].content)
