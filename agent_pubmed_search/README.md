![domain:innovation-lab](https://img.shields.io/badge/innovation--lab-3D8BD3)
![domain:research](https://img.shields.io/badge/research-3D8BD3)

**Description**: This AI Agent searches PubMed for research papers based on a given query. It retrieves relevant publications, including their titles, authors, and direct links to PubMed. This agent is useful for researchers, students, and professionals looking to quickly find scientific literature related to a specific topic.

**Input Data Model**
```python
class initRARequest(Model):
    query: str
    sender_address: str  
```

**Output Data Model**
```python
class initRAResponse(Model):
    results: list
```

**Functionality**:
- The agent receives a search query from a user.
- It queries the PubMed database for relevant papers.
- It extracts key details, including the title, author(s), and a link to the publication.
- It returns a list of matching publications as a response.

**How to Use**:
1. Deploy the PubMed Agent using the command:
   ```sh
   python pubmed_agent.py
   ```
2. Send a message to the agent with a search query.
3. Receive a response containing a list of relevant PubMed papers.

**Example Request**:
```python
request = initRARequest(query="Deepfake detection in medicine", sender_address="agent_123")
```

**Example Response**:
```python
response = initRAResponse(results=[
    {
        "title": "Deep Learning for Medical Deepfake Detection",
        "authors": ["John Doe", "Jane Smith"],
        "link": "https://pubmed.ncbi.nlm.nih.gov/12345678/"
    }
])
```

**Deployment Instructions**:
- Ensure you have `Bio` installed:
  ```sh
  pip install Bio
  ```
- Run the agent with the correct configurations.
- Replace `your_email@example.com` in the code with a valid email address for PubMed API access.

This agent streamlines research by automating PubMed searches and providing structured results.

