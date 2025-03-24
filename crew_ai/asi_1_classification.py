import os
import requests
from uagents import Agent, Context, Model
from crewai import Agent as CrewAIAgent, Task, Crew, Process

ASI1_API_KEY = ""
ASI1_URL = "https://api.asi1.ai/v1/chat/completions"

# Define the get_asi1_response function
def get_asi1_response(query: str) -> str:
    """
    Sends a query to ASI1 API and returns the response.
    """
    headers = {
        "Authorization": f"Bearer {ASI1_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "asi1-mini",  # Select appropriate ASI1 model
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": query}
        ]
    }

    try:
        response = requests.post(ASI1_URL, json=data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"].strip()
            else:
                return "ASI1 API returned an empty response."
        else:
            return f"ASI1 API Error: {response.status_code}, {response.text}"
    except Exception as e:
        return f"ASI1 API Error: {str(e)}"

# Define custom search tool to interact with ASI1 API
class ASI1SearchTool:
    def search(self, information: str) -> str:
        # Format query based on the information
        query = f"Analyze the following information and determine if it is real or fake: '{information}'. Use credible sources to validate its authenticity."
        return get_asi1_response(query)

# Define agent and replace SerperDevTool with ASI1SearchTool
senior_information_analyst_agent = Agent(
    name="information_analyst_agent",
    seed="information_analyst_agent_seed",
    port=8001,
    endpoint=["http://127.0.0.1:8001/submit"],
)

class InformationRequestModel(Model):
    information: str

class AnalysisReportModel(Model):
    analysis: str

class SeniorInformationAnalyst:
    def __init__(self):
        """
        Initializes the Senior Information Analyst agent with a search tool.
        """
        self.search_tool = ASI1SearchTool()  # Use custom search tool here

        self.analyst = CrewAIAgent(
            role="Senior Information Analyst",
            goal="Analyze given information and determine if it is fake or real.",
            backstory="""You are an expert in identifying misinformation.
            Your job is to verify the authenticity of claims using available online sources.""",
            verbose=True,
            allow_delegation=False,
            tools=[self.search_tool],
        )

    def create_task(self, information: str) -> Task:
        """
        Creates a task to analyze the authenticity of the given information.

        Parameters:
        - information: str, the information to be analyzed.

        Returns:
        - Task: The created task with the specified description and expected output.
        """
        task_description = (
            f"Analyze the following information and determine if it is real or fake: '{information}'."
            f"Use credible sources to validate its authenticity."
        )

        expected_output = "Detailed analysis report indicating whether the information is real or fake."

        # Search query formatted with task description
        search_query = f"{task_description} Provide supporting evidence and relevant sources."

        return Task(
            description=task_description,
            expected_output=expected_output,
            agent=self.analyst,
            tool=self.search_tool.search(information)  # Trigger the ASI1 search tool for the query
        )

    def run_process(self, information: str):
        """
        Runs the process for the created task and retrieves the result.

        Parameters:
        - information: str, the information to be analyzed.

        Returns:
        - result: The output from the CrewAI process after executing the task.
        """
        task = self.create_task(information)
        crew = Crew(
            agents=[self.analyst],
            tasks=[task],
            verbose=True,
            process=Process.sequential,
        )
        result = crew.kickoff()
        return result

@senior_information_analyst_agent.on_message(model=InformationRequestModel, replies=AnalysisReportModel)
async def handle_information_request(ctx: Context, sender: str, msg: InformationRequestModel):
    """
    Handles incoming messages requesting information analysis.

    What it does:
    - Logs the received information.
    - Runs the analysis process and sends the report back to the sender.

    Parameters:
    - ctx: Context, provides the execution context for logging and messaging.
    - sender: str, the address of the sender agent.
    - msg: InformationRequestModel, the received message containing the information.

    Returns:
    - None: Sends the analysis report to the sender agent.
    """
    ctx.logger.info(f"Received message from {sender} with information: {msg.information}")
    analyst = SeniorInformationAnalyst()
    analysis_result = analyst.run_process(msg.information)
    await ctx.send(sender, AnalysisReportModel(analysis=str(analysis_result)))

if __name__ == "__main__":
    """
    Starts the communication agent and begins listening for messages.

    What it does:
    - Runs the agent, enabling it to send/receive messages and handle events.

    Returns:
    - None: Runs the agent loop indefinitely.
    """
    senior_information_analyst_agent.run()
