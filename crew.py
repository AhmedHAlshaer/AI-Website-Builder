import os
from crewai import Crew, Agent, Task, Process, agent, task, crew, LLM
from crewai.project import CrewBase
from tools import make_dir, write_file, append_file, exists

# Use DeepSeek as the LLM provider via environment variables (no hard-coded API keys)
model_name = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    raise RuntimeError("DEEPSEEK_API_KEY environment variable is not set.")
# Initialize the DeepSeek LLM with the given model and API endpoint
llm = LLM(model=model_name, api_key=api_key, base_url="https://api.deepseek.com/v1")

# Define the Crew with agents and tasks
class SiteBuilderCrew(CrewBase):
    # Specify configuration files for agents and tasks
    agents_config = "agents.yaml"
    tasks_config = "tasks.yaml"

    @agent
    def team_lead(self) -> Agent:
        return Agent(config=self.agents_config["team_lead"], llm=llm)

    @agent
    def frontend_dev(self) -> Agent:
        return Agent(config=self.agents_config["frontend_dev"], llm=llm)

    @agent
    def backend_dev(self) -> Agent:
        return Agent(config=self.agents_config["backend_dev"], llm=llm)

    @agent
    def integrator(self) -> Agent:
        # The integrator agent has access to file system tools to write the project files
        return Agent(config=self.agents_config["integrator"], llm=llm, tools=[make_dir, write_file, append_file, exists])

    @agent
    def tester(self) -> Agent:
        return Agent(config=self.agents_config["tester"], llm=llm)

    @task
    def plan(self) -> Task:
        return Task(config=self.tasks_config["plan"], agent=self.team_lead())

    @task
    def develop_frontend(self) -> Task:
        return Task(config=self.tasks_config["develop_frontend"], agent=self.frontend_dev())

    @task
    def develop_backend(self) -> Task:
        return Task(config=self.tasks_config["develop_backend"], agent=self.backend_dev())

    @task
    def integrate_code(self) -> Task:
        return Task(config=self.tasks_config["integrate_code"], agent=self.integrator())

    @task
    def test_run(self) -> Task:
        return Task(config=self.tasks_config["test_run"], agent=self.tester())

    @crew
    def crew(self) -> Crew:
        # Run tasks sequentially in the defined order
        return Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential, verbose=True)
