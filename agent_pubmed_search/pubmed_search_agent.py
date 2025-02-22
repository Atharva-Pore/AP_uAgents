from uagents import Agent, Context, Model
from Bio import Entrez
import json

# Define the input model class
class initRARequest(Model):
    query: str
    sender_address: str  

# Define a common response model
class initRAResponse(Model):
    results: list

# Create the PubMed agent
pubmed_agent = Agent(
    name="PubMedAgent",
    port=5057,
    seed="pubmed_seed",
    endpoint="http://localhost:5057/submit"
)

def search_pubmed(query, max_results=5):
    """Searches PubMed for papers related to the given query."""
    Entrez.email = "your_email@example.com"  

    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    handle.close()
    
    pubmed_ids = record["IdList"]
    
    results = []
    for pubmed_id in pubmed_ids:
        summary = Entrez.efetch(db="pubmed", id=pubmed_id, retmode="xml")
        paper = Entrez.read(summary)
        
        title = paper["PubmedArticle"][0]["MedlineCitation"]["Article"]["ArticleTitle"]
        authors = paper["PubmedArticle"][0]["MedlineCitation"]["Article"]["AuthorList"]
        authors = [f"{a['ForeName']} {a['LastName']}" for a in authors if "ForeName" in a and "LastName" in a]
        link = f"https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}/"

        results.append({
            "title": title,
            "authors": authors,
            "link": link,
        })
    
    return results

# Handle incoming search requests
@pubmed_agent.on_message(model=initRARequest)
async def handle_pubmed_search(ctx: Context, sender: str, msg: initRARequest):
    ctx.logger.info(f"Received search request for query: {msg.query} from {sender}")
    
    results = search_pubmed(msg.query)

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
    await ctx.send(sender, response)

if __name__ == "__main__":
    pubmed_agent.run()
