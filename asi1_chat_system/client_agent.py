from uagents import Agent, Context, Model

# Query model to send to the server agent
class ASI1Query(Model):
    query: str
    sender_address: str

# Response model to receive from the server agent
class ASI1Response(Model):
    response: str

# Client agent setup
clientAgent = Agent(
    name='asi1_client_agent',
    port=5070,
    endpoint='http://localhost:5070/submit',
    seed='asi1_client_seed'
)

# Server agent address (update with actual address if needed)
SERVER_AGENT_ADDRESS = "agent1q0usc8uc5hxes4ckr8624ghdxpn0lvxkgex44jtfv32x2r7ymx8sgg8yt2g"  # Replace with the actual address of your server agent

@clientAgent.on_event('startup')
async def startup_handler(ctx: Context):
    ctx.logger.info(f'Client Agent {ctx.agent.name} started at {ctx.agent.address}')

    # Get user input
    user_query = input("Ask something: ")

    # Send the query to the server agent
    await ctx.send(SERVER_AGENT_ADDRESS, ASI1Query(query=user_query, sender_address=ctx.agent.address))
    ctx.logger.info(f"Query sent to server agent: {user_query}")

@clientAgent.on_message(model=ASI1Response)
async def handle_response(ctx: Context, sender: str, msg: ASI1Response):
    ctx.logger.info(f"Response received from {sender}: {msg.response}")

# Run the client agent
if __name__ == "__main__":
    clientAgent.run()
