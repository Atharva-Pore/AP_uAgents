from uagents import Agent, Context, Model
from scholarly import scholarly
import json

# Define the input model class
class initRARequest(Model):
    query: str
    sender_address: str  

# Define a common response model
class initRAResponse(Model):
    results: list

# Create the Google Scholar agent
google_scholar_agent = Agent(
    name="GoogleScholarAgent",
    port=5056,
    seed="google_scholar_seed",
    endpoint="http://localhost:5056/submit"
)

def search_google_scholar(query, max_results=5):
    """Searches Google Scholar for papers related to the given query."""
    search_query = scholarly.search_pubs(query)
    
    results = []
    for i in range(max_results):
        try:
            paper = next(search_query)
            results.append({
                "title": paper["bib"]["title"],
                "authors": paper["bib"].get("author", "Unknown"),
                "link": paper.get("pub_url", "No link available"),
                "year": paper["bib"].get("pub_year", "Unknown"),
            })
        except StopIteration:
            break

    return results

# Handle incoming search requests
@google_scholar_agent.on_message(model=initRARequest)
async def handle_google_scholar_search(ctx: Context, sender: str, msg: initRARequest):
    ctx.logger.info(f"Received search request for query: {msg.query} from {msg.sender_address}")
    
    results = search_google_scholar(msg.query)
    response = initRAResponse(results=results)
    # if len(results) > 0:
    #     response = initRAResponse(results=results)
    # else:
    #     response = [json.dumps({
    #         "title": 'NA',
    #         "authors": 'NA',
    #         "link": 'NA',
    #     })]
    
    # Send results back to the requesting agent
    await ctx.send(msg.sender_address, response)

if __name__ == "__main__":
    google_scholar_agent.run()
