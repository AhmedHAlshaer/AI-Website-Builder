import os

from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import CrewBase, agent, task, crew
from builder.tools import (
    make_dir, 
    write_file, 
    append_file, 
    exists,
    read_file,
    list_dir,
    file_contains
)

model_name = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    raise RuntimeError("DEEPSEEK_API_KEY environment variable is not set.")

llm = LLM(model = model_name, api_key = api_key, base_url = "https://api.deepseek.com/v1")


@CrewBase
class EditorCrew():
    """Editor that edits existing websites according to what a user wants"""
    
    agents_config = "config/agents.yaml"
    tasks_config = "config/editor_tasks.yaml"
    
    @agent
    def analyzer(self):
        """Editor analyzer"""
        return Agent(
            config = self.agents_config["analyzer"],
            llm = llm,
            verbose = True,
            tools = [read_file, list_dir, exists, file_contains]
        )
    
    @agent
    def editor(self):
        """An editor agent"""
        return Agent(
            config = self.agents_config["editor"],
            llm = llm,
            verbose = True
        )
    
    @agent 
    def integrator(self):
        """Integrator Agent"""
        return Agent(
            config = self.agents_config["integrator"],
            llm = llm,
            verbose = True,
            tools = [make_dir, write_file, append_file, exists]
        )
    
    @agent 
    def tester(self):
        """Tester agent"""
        return Agent(
            config = self.agents_config["tester"],
            llm = llm,
            verbose = True,
            tools = [read_file, list_dir, exists, file_contains]
        )

    @task
    def analyze_existing(self):
        """Create analyzing tasks"""
        return Task(
            config = self.tasks_config["analyze_existing"],
            agent = self.analyzer()
        )
    
    @task
    def plan_modifications(self):
        """Creates edited files"""

        return Task(
            config = self.tasks_config['plan_modifications'],
            agent = self.editor(),
            context = [self.analyze_existing()]
        )

    @task
    def integrate_code(self):
        """Over Write files"""
        return Task(
            config = self.tasks_config["integrate_code"],
            agent = self.integrator(),
            context = [self.analyze_existing(), self.plan_modifications()]
        )
    
    @task 
    def test_run(self):
        """Tests code"""

        return Task(
            config = self.tasks_config["test_run"],
            agent = self.tester(),
            context = [self.analyze_existing(), self.plan_modifications(), self.integrate_code()]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the editor crew"""

        return Crew(
            agents = self.agents,
            tasks = self.tasks, 
            process = Process.sequential,
            verbose = True
        )

    

