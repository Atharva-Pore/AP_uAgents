import requests
from uagents import Agent, Context, Model

# ASI1 API Configuration
ASI1_API_KEY = "sk_59225cd35f384d529c2cbcb19e4a29dcae64ca00e1c84220a358712ebd0efd9c"  # Replace with your API key
ASI1_URL = "https://api.asi1.ai/v1/chat/completions"

# Request model
class ASI1Query(Model):
    query: str
    sender_address: str

# Response model
class ASI1Response(Model):
    response: str  # Response from ASI1 API

# Define the main agent
mainAgent = Agent(
    name='asi1_chat_agent',
    port=5068,
    endpoint='http://localhost:5068/submit',
    seed='asi1_chat_seed'
)

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
            {"role": "user", "content":  f"Search hugging face pipelines or transformers or models for {query}"}
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

@mainAgent.on_event('startup')
async def startup_handler(ctx: Context):
    ctx.logger.info(f'Agent {ctx.agent.name} started at {ctx.agent.address}')

# Handler for receiving query
@mainAgent.on_message(model=ASI1Query)
async def handle_query(ctx: Context, sender: str, msg: ASI1Query):
    ctx.logger.info(f"Received query from {sender}: {msg.query}")

    # Call ASI1 API for the response
    answer = get_asi1_response(msg.query)

    # Respond back with the answer from ASI1
    await ctx.send(sender, ASI1Response(response=answer))

# Run the agent
if __name__ == "__main__":
    mainAgent.run()
