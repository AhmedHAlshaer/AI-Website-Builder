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

# Use DeepSeek as the LLM provider via environment variables (no hard-coded API keys)
model_name = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    raise RuntimeError("DEEPSEEK_API_KEY environment variable is not set.")

# Initialize the DeepSeek LLM with the given model and API endpoint
llm = LLM(model=model_name, api_key=api_key, base_url="https://api.deepseek.com/v1")


# Define the Crew with agents and tasks
@CrewBase
class SiteBuilderCrew():
    """SiteBuilder crew for building websites from user requirements"""
    
    # Specify configuration files for agents and tasks
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def team_lead(self) -> Agent:
        """Project planning agent"""
        return Agent(
            config=self.agents_config["team_lead"], 
            llm=llm,
            verbose=True
        )

    @agent
    def frontend_dev(self) -> Agent:
        """Frontend development agent"""
        return Agent(
            config=self.agents_config["frontend_dev"], 
            llm=llm,
            verbose=True
        )

    @agent
    def backend_dev(self) -> Agent:
        """Backend development agent"""
        return Agent(
            config=self.agents_config["backend_dev"], 
            llm=llm,
            verbose=True
        )

    @agent
    def integrator(self) -> Agent:
        """Integration agent with file system tools"""
        return Agent(
            config=self.agents_config["integrator"], 
            llm=llm,
            tools=[make_dir, write_file, append_file, exists],
            verbose=True
        )

    @agent
    def tester(self) -> Agent:
        """QA agent with file inspection tools"""
        return Agent(
            config=self.agents_config["tester"], 
            llm=llm,
            tools=[exists, read_file, list_dir, file_contains],
            verbose=True
        )

    @task
    def plan(self) -> Task:
        """Create project plan task"""
        return Task(
            config=self.tasks_config["plan"],
            agent=self.team_lead()
        )

    @task
    def develop_frontend(self) -> Task:
        """Develop frontend code task"""
        return Task(
            config=self.tasks_config["develop_frontend"],
            agent=self.frontend_dev()
        )

    @task
    def develop_backend(self) -> Task:
        """Develop backend code task"""
        return Task(
            config=self.tasks_config["develop_backend"],
            agent=self.backend_dev()
        )

    @task
    def integrate_code(self) -> Task:
        """Integrate all code into project structure task"""
        return Task(
            config=self.tasks_config["integrate_code"],
            agent=self.integrator()
        )

    @task
    def test_run(self) -> Task:
        """Test and verify generated website task"""
        return Task(
            config=self.tasks_config["test_run"],
            agent=self.tester()
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SiteBuilder crew"""
        # Run tasks sequentially in the defined order
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )