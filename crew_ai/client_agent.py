from uagents import Agent, Context, Model


class InformationRequestModel(Model):
    information: str


class AnalysisReportModel(Model):
    analysis: str


client_agent = Agent(
    name="client_agent",
    seed="client_agent_seed",
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

# TARGET_AGENT_ADDRESS = (
#     "agent1qfjzc479lamv7a44dln3ln5kv3hyfqfj9a8pcr4zy6qrs4gkf2av64dxsxc"
# )

TARGET_AGENT_ADDRESS = (
    "agent1qfjzc479lamv7a44dln3ln5kv3hyfqfj9a8pcr4zy6qrs4gkf2av64dxsxc"
)


@client_agent.on_event("startup")
async def on_startup(ctx: Context):
    """
    Triggered when the agent starts up.

    What it does:
    - Logs the agent's name and address.
    - Takes input from the user.
    - Sends a message to the senior info analyst agent with the provided information.

    Parameters:
    - ctx: Context, provides the execution context for logging and messaging.

    Returns:
    - None: Sends the message to the target agent asynchronously.
    """
    ctx.logger.info(
        f"Hello, I'm {client_agent.name}, and my address is {client_agent.address}."
    )
    
    user_input = input("Enter the information to be analyzed: ")
    await ctx.send(TARGET_AGENT_ADDRESS, InformationRequestModel(information=user_input))


@client_agent.on_message(model=AnalysisReportModel)
async def handle_analysis_report(ctx: Context, sender: str, msg: AnalysisReportModel):
    """
    Triggered when a message of type AnalysisReportModel is received.

    What it does:
    - Logs the sender's address and the analysis report received.

    Parameters:
    - ctx: Context, provides the execution context for logging and messaging.
    - sender: str, the address of the sender agent.
    - msg: AnalysisReportModel, the received analysis report.

    Returns:
    - None: Processes the message and logs it.
    """
    ctx.logger.info(f"Received analysis report from {sender}: {msg.analysis}")


if __name__ == "__main__":
    """
    Starts the client agent and begins listening for events.

    What it does:
    - Runs the agent, enabling it to send/receive messages and handle events.

    Returns:
    - None: Runs the agent loop indefinitely.
    """
    client_agent.run()
