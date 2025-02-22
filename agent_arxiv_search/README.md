![domain:innovation-lab](https://img.shields.io/badge/innovation--lab-3D8BD3)
![domain:research](https://img.shields.io/badge/research-3D8BD3)

**Description**: This AI Agent retrieves the latest research papers from [ArXiv](https://arxiv.org/) based on a given query. It allows users to search for academic papers related to Artificial Intelligence, Machine Learning, Physics, Mathematics, and more. The agent returns details such as paper titles, authors, publication dates, and direct links to the research papers.

**Usage**: Users can send a search query to the agent, and it will return a list of relevant research papers from ArXiv.

---

### **Input Data Model**
```python
class initRARequest(Model):
    query: str
    sender_address: str
```
**Fields:**
- `query`: The search term for finding relevant papers.
- `sender_address`: The address of the sender requesting the search.

---

### **Output Data Model**
```python
class initRAResponse(Model):
    results: list
```
**Fields:**
- `results`: A list of dictionaries containing details of the retrieved research papers, including:
  - `title`: Title of the paper.
  - `authors`: List of author names.
  - `link`: URL to the paper.
  - `published`: The publication date of the paper.

---

### **Example Request & Response**
#### **Request:**
```json
{
    "query": "deep learning",
    "sender_address": "agent1qxyz..."
}
```

#### **Response:**
```json
{
    "results": [
        {
            "title": "An Overview of Deep Learning",
            "authors": ["Ian Goodfellow", "Yoshua Bengio", "Aaron Courville"],
            "link": "https://arxiv.org/abs/1234.56789",
            "published": "2024-02-15"
        },
        {
            "title": "Deep Reinforcement Learning: A Survey",
            "authors": ["David Silver", "Richard Sutton"],
            "link": "https://arxiv.org/abs/9876.54321",
            "published": "2023-11-10"
        }
    ]
}
```

---

### **Deployment Instructions**
1. Install dependencies:
   ```bash
   pip install uagents arxiv
   ```
2. Run the agent:
   ```bash
   python arxiv_agent.py
   ```

---

### **Use Cases**
- Researchers looking for the latest publications in their field.
- Students searching for reference papers for their projects.
- Developers integrating AI-driven research discovery tools.

---

### **Notes**
- The agent fetches results from ArXiv in real-time.
- It returns the most recent papers sorted by submission date.
- Maximum number of results returned per query is **5** (can be adjusted in the code).

---

**Developed by:** [Atharva Pore](https://www.linkedin.com/in/atharva-pore/)

