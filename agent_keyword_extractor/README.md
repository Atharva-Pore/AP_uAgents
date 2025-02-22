![domain:innovation-lab](https://img.shields.io/badge/innovation--lab-3D8BD3)
![domain:nlp](https://img.shields.io/badge/nlp-3D8BD3)
![domain:research](https://img.shields.io/badge/nlp-3D8BD3)
![domain:keyword extractor](https://img.shields.io/badge/nlp-3D8BD3)

# KeywordExtractionAgent

## Description
The `KeywordExtractionAgent` is an AI-powered agent that extracts the most important keywords from a given text. It utilizes both OpenAI's GPT model and the KeyBERT model to ensure accurate and comprehensive keyword extraction. This agent is useful for research, text analysis, content summarization, and SEO optimization.

## How It Works
Users can send a text input to the agent, and it will process the input using two different methods:
1. **OpenAI GPT-4o**: Extracts keywords using natural language understanding.
2. **KeyBERT**: Identifies the most relevant keywords using BERT embeddings.

The agent then combines the results from both methods, removes duplicates, and returns a list of extracted keywords.

## Input Data Model
```python
class KeywordExtractionRequest(Model):
    text: str
```
- `text`: A string containing the input text from which keywords need to be extracted.

## Output Data Model
```python
class KeywordExtractionResponse(Model):
    keywords: list
```
- `keywords`: A list of extracted keywords from the input text.

## Example Usage
1. A user sends a request:
   ```python
   KeywordExtractionRequest(text="Machine learning is a field of artificial intelligence that enables computers to learn from data.")
   ```
2. The agent processes the request and responds with extracted keywords:
   ```python
   KeywordExtractionResponse(keywords=["machine learning", "artificial intelligence", "computers", "data"])
   ```

## Deployment
To run the agent locally, execute:
```bash
python keyword_extraction_agent.py
```

## Use Cases
- **Text Summarization**: Extracts key topics from long articles.
- **SEO Optimization**: Helps identify relevant keywords for content ranking.
- **Research Assistance**: Automatically highlights essential terms in academic papers.
- **Content Categorization**: Useful for tagging and organizing textual data.

## Contact & Support
For any issues or feature requests, feel free to reach out or submit an issue on the repository!

