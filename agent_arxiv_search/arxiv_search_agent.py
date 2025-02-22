from uagents import Agent, Context, Model
import arxiv
import json

# Define the input model for the search request
class initRARequest(Model):
    query: str
    sender_address: str

# Define a common response model
class initRAResponse(Model):
    results: list

# Create the ArXiv agent
arxiv_agent = Agent(
    name="ArxivAgent",
    port=5055,
    endpoint="http://localhost:5055/submit",
    seed="arxiv_search_seed_12345",
)

def search_arxiv_papers(query, max_results=5):
    """Searches ArXiv for papers related to the given query."""
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    results = []
    for paper in search.results():
        results.append({
            "title": paper.title,
            "authors": [author.name for author in paper.authors],
            "link": paper.entry_id,
            "published": paper.published.strftime("%Y-%m-%d"),
        })

    return results

@arxiv_agent.on_message(model=initRARequest)
async def handle_pubmed_search(ctx: Context, sender: str, msg: initRARequest):
    """Handles incoming search requests and returns results."""
    ctx.logger.info(f"Received search request for query: {msg.query} from {msg.sender_address}")

    results = search_arxiv_papers(msg.query)

    response = initRAResponse(results=results)

    await ctx.send(msg.sender_address, response)

if __name__ == "__main__":
    arxiv_agent.run()
