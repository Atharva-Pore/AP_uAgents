![domain:innovation-lab](https://img.shields.io/badge/innovation--lab-3D8BD3)
![domain:research](https://img.shields.io/badge/research-3D8BD3)

**Description**:  The Google Scholar Agent is an AI-powered research assistant that retrieves academic papers from Google Scholar based on user queries. This agent helps researchers, students, and professionals find relevant scholarly articles, including details like title, authors, publication year, and links to sources. Simply input a search query, and the agent will return a curated list of relevant research papers.

---

### **Input Data Model**
```python
class initRARequest(Model):
    query: str
    sender_address: str  
```
- `query`: The search term or topic for retrieving academic papers.
- `sender_address`: The address of the requesting agent.

---

### **Output Data Model**
```python
class initRAResponse(Model):
    results: list
```
Each result contains:
- `title`: The title of the research paper.
- `authors`: The names of the authors (if available).
- `link`: A direct link to the paper (if available).
- `year`: The publication year of the paper (if available).

---

### **How It Works**
1. The agent listens for requests containing a search query.
2. It queries Google Scholar and retrieves relevant academic papers.
3. The results, including paper details, are sent back to the requesting agent.

---

### **Usage Example**
#### **Request Example:**
```json
{
    "query": "deepfake detection using CNN",
    "sender_address": "agent_123"
}
```

#### **Response Example:**
```json
{
    "results": [
        {
            "title": "Deepfake Detection Using Convolutional Neural Networks",
            "authors": "John Doe, Jane Smith",
            "link": "https://scholar.google.com/somepaper",
            "year": "2023"
        },
        {
            "title": "Advancements in Deepfake Identification",
            "authors": "Alice Brown, Bob Johnson",
            "link": "https://scholar.google.com/anotherpaper",
            "year": "2022"
        }
    ]
}
```

---

### **Deployment & Execution**
To run the Google Scholar Agent locally:
```bash
python google_scholar_agent.py
```
Ensure that all dependencies, including `uagents` and `scholarly`, are installed before running the agent.

---

### **Use Cases**
- **Academic Research:** Quickly find relevant papers for literature reviews.
- **Industry Professionals:** Stay updated with the latest research trends in your domain.
- **Students:** Easily gather references for projects and assignments.

This agent streamlines the research process by automating academic paper searches, making knowledge discovery more efficient and accessible!

