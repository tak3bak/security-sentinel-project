from crewai import Agent, Task, Crew, Process
from langchain_ollama import OllamaLLM
from tools import FileManagementTools

# Initialize Local LLM
llm = OllamaLLM(model="llama3")

# Initialize Tools
file_tools = [FileManagementTools.read_file, FileManagementTools.write_file]

# Define Agents
writer = Agent(
    role='Technical Writer',
    goal='Refine documentation and code comments.',
    backstory='You are a precise technical writer who updates project files.',
    tools=file_tools,
    llm=llm
)

reviewer = Agent(
    role='Senior Editor',
    goal='Ensure all technical writing is accurate and concise.',
    backstory='You provide actionable feedback and approve final drafts.',
    llm=llm
)

# Workflow Definition
# This workflow now has the capability to modify your local directory
