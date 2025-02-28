from uagents import Agent, Context, Model
from keybert import KeyBERT
import openai

# OpenAI API Key (Ensure to use your own secure key)
OPEN_AI_KEY = 'your_openai_key'

# Define the input model
class KeywordExtractionRequest(Model):
    text: str

# Define the response model
class KeywordExtractionResponse(Model):
    keywords: list

# Create the Keyword Extraction Agent
keyword_agent = Agent(
    name="KeywordExtractionAgent",
    port=5058,
    seed="keyword_extraction_seed",
    endpoint="http://localhost:5058/submit"
)

def extract_keywords_openai(text: str, openai_api_key: str = OPEN_AI_KEY, model: str = "gpt-4o") -> list:
    """
    Extracts keywords from a given text using OpenAI's GPT model.
    """
    try:
        openai.api_key = openai_api_key  # Set API key for OpenAI
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "Extract the most important keywords from the given text."},
                {"role": "user", "content": text},
            ],
            max_tokens=100,
        )
        extracted_text = response['choices'][0]['message']['content']
        keywords = [keyword.strip() for keyword in extracted_text.split("\n") if keyword.strip()]
        return keywords
    except Exception as e:
        return [f"Error: {str(e)}"]

def extract_keywords_keybert(text: str, top_n: int = 5) -> list:
    """
    Extracts keywords using the KeyBERT model.
    """
    kw_model = KeyBERT()
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 3), stop_words='english', top_n=top_n)
    return [keyword[0] for keyword in keywords]

# Handle incoming keyword extraction requests
@keyword_agent.on_message(model=KeywordExtractionRequest)
async def handle_keyword_extraction(ctx: Context, sender: str, msg: KeywordExtractionRequest):
    ctx.logger.info(f"Received keyword extraction request from {sender}")
    
    openai_keywords = extract_keywords_openai(msg.text)
    keybert_keywords = extract_keywords_keybert(msg.text)
    
    combined_keywords = list(set(openai_keywords + keybert_keywords))  # Remove duplicates
    
    response = KeywordExtractionResponse(keywords=combined_keywords)
    await ctx.send(sender, response)

if __name__ == "__main__":
    keyword_agent.run()
