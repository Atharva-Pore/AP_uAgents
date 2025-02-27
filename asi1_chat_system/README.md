![domain:innovation-lab](https://img.shields.io/badge/innovation--lab-3D8BD3)
![domain:LLM](https://img.shields.io/badge/research-3D8BD3)

**Description**: The ASI1 Chat Agent is an AI-powered assistant that interacts with the ASI1 API to retrieve responses based on user queries. This agent is designed to facilitate AI-based searches for Hugging Face pipelines, transformers, or models, making it useful for researchers, developers, and AI enthusiasts.

---

### **Input Data Model**
```python
class ASI1Query(Model):
    query: str
    sender_address: str  
```
- `query`: The search term or topic for retrieving AI-related information.
- `sender_address`: The address of the requesting agent.

---

### **Output Data Model**
```python
class ASI1Response(Model):
    response: str
```
- `response`: The AI-generated response retrieved from the ASI1 API.

---

### **How It Works**
1. The client agent sends a query to the server agent.
2. The server agent processes the request and queries the ASI1 API.
3. The ASI1 API returns a response, which is sent back to the client agent.
4. The client agent receives and displays the response.

---

### **Usage Example**
#### **Request Example:**
```json
{
    "query": "best Hugging Face transformer for text classification",
    "sender_address": "agent_123"
}
```

#### **Response Example:**
```json
{
    "response": "The best Hugging Face transformer for text classification depends on the dataset and requirements. Popular choices include BERT, RoBERTa, and DistilBERT."
}
```

---

### **Deployment & Execution**
#### **Running the Server Agent:**
```bash
python asi1_chat_agent.py
```

#### **Running the Client Agent:**
```bash
python asi1_client_agent.py
```
Ensure that all dependencies, including `uagents` and `requests`, are installed before running the agents.

---

### **Use Cases**
- **AI Research:** Quickly find relevant AI models and tools.
- **Developers:** Retrieve insights on Hugging Face pipelines.
- **Students & Enthusiasts:** Learn about AI model selection and implementation.

This agent simplifies AI-related searches, making it easier to find and use cutting-edge models in various applications!

