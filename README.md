# Multi-Agent Customer Service System with A2A and MCP

A production-ready multi-agent customer service system demonstrating Agent-to-Agent (A2A) communication and Model Context Protocol (MCP) integration using LangGraph.

## 📋 Overview

This system implements three specialized agents that coordinate to handle customer service queries:

- **Router Agent (Orchestrator)**: Analyzes queries, extracts intent, routes to appropriate agents
- **Customer Data Agent (Specialist)**: Accesses customer database via MCP protocol
- **Support Agent (Specialist)**: Handles support queries with customer context

### Key Features

✅ **MCP Integration**: 5 standardized tools for database access
✅ **A2A Coordination**: Three coordination patterns (Task Allocation, Negotiation, Multi-Step)
✅ **Explicit Logging**: Complete A2A communication tracking
✅ **LangGraph Workflow**: Conditional routing and state management
✅ **5 Test Scenarios**: Comprehensive demonstrations

## 🛠️ Installation

### Prerequisites

- Python 3.10 or higher
- OpenAI API key
- Virtual environment recommended

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/Multi-Agent-Customer-Service-System-with-A2A-and-MCP.git
cd Multi-Agent-Customer-Service-System-with-A2A-and-MCP
```

2. **Create and activate virtual environment**

On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows:
```bash
python -m venv venv
venv\\Scripts\\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up OpenAI API key**

Create a `.env` file or set environment variable:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

Or in Python:
```python
import os
os.environ["OPENAI_API_KEY"] = "your-api-key-here"
```

5. **Initialize database**
```bash
python database_setup.py
```

This will create `customer_service.db` with test data.

## 🚀 Usage

### Option 1: Jupyter Notebook (Recommended)

1. Start Jupyter:
```bash
jupyter notebook
```

2. Open `Multi_Agent_Customer_Service_Complete.ipynb`

3. Run all cells sequentially

4. Explore the 3 coordination scenarios and 5 test cases

### Option 2: Python Scripts

**Test MCP Server:**
```bash
python mcp_server.py
```

**Run custom queries:**
```python
from mcp_server import MCPServer

# Initialize
mcp = MCPServer("customer_service.db")

# Use MCP tools
customer = mcp.get_customer(1)
history = mcp.get_customer_history(1)
customers = mcp.list_customers(status="active", limit=5)
```

## 📁 Project Structure

```
Multi-Agent-Customer-Service-System-with-A2A-and-MCP/
│
├── Multi_Agent_Customer_Service_Complete.ipynb  # Main notebook
├── database_setup.py                            # Database initialization
├── mcp_server.py                                # MCP server implementation
├── requirements.txt                             # Python dependencies
├── README.md                                    # This file
├── customer_service.db                          # SQLite database (created)
│
└── Colab_Notebook_Agentic_Patterns_with_LangGraph_Dr_Fouad_Bousetouane.ipynb
    # Reference notebook for LangGraph patterns
```

## 🧪 Test Scenarios

The notebook includes 5 comprehensive test scenarios:

### 1. Simple Query
**Query:** "Get customer information for ID 5"
**Flow:** Router → Data Agent → Response
**Tests:** Single agent routing

### 2. Coordinated Query
**Query:** "I'm customer 1 and need help upgrading my account"
**Flow:** Router → Data Agent (context) → Support Agent → Response
**Tests:** Multi-agent coordination with context sharing

### 3. Complex Query
**Query:** "Show me all active customers who have open tickets"
**Flow:** Router → Data Agent (multiple MCP calls) → Report
**Tests:** Multi-step coordination

### 4. Escalation
**Query:** "I've been charged twice, please refund immediately!"
**Flow:** Router → Data Agent → Support Agent (urgency detection)
**Tests:** Priority handling and escalation detection

### 5. Multi-Intent
**Query:** "Update my email to new@email.com and show my ticket history"
**Flow:** Router → Parallel execution (update + retrieve)
**Tests:** Parallel task execution

## 🔄 A2A Coordination Patterns

### Pattern 1: Task Allocation
Router analyzes query and delegates to single specialist agent.

```
Router → [Analyze Intent] → Data Agent → Response
```

### Pattern 2: Negotiation/Escalation
Multiple agents coordinate when query has multiple intents.

```
Router → [Detect Multi-Intent] → Data Agent → Support Agent → Synthesize
```

### Pattern 3: Multi-Step Coordination
Complex queries decomposed into sub-tasks.

```
Router → [Decompose] → Data (Step 1) → Data (Step 2) → Synthesize Report
```

## 📊 MCP Server Tools

The system implements 5 MCP tools:

| Tool | Description | Usage |
|------|-------------|-------|
| `get_customer(customer_id)` | Retrieve customer by ID | Data lookups |
| `list_customers(status, limit)` | List customers with filters | Batch operations |
| `update_customer(customer_id, data)` | Update customer record | Account modifications |
| `create_ticket(customer_id, issue, priority)` | Create support ticket | Issue tracking |
| `get_customer_history(customer_id)` | Get full customer history | Context gathering |

## 🗄️ Database Schema

### Customers Table
```sql
CREATE TABLE customers (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    email           TEXT,
    phone           TEXT,
    status          TEXT DEFAULT 'active',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Tickets Table
```sql
CREATE TABLE tickets (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id     INTEGER NOT NULL,
    issue           TEXT NOT NULL,
    status          TEXT DEFAULT 'open',
    priority        TEXT DEFAULT 'medium',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
)
```

## 🔍 A2A Communication Logging

Every agent interaction is logged for transparency:

```python
[ROUTER] Analyzed query - Intent: account_info
[ROUTER → DATA] Requesting customer data
[DATA] Calling MCP: get_customer_history(1)
[DATA → SUPPORT] Providing customer context for Alice Johnson
[SUPPORT] Using customer context from Data Agent
[SUPPORT → ROUTER] Generated response
[ROUTER] Finalized response
```

## 🎓 Learning Outcomes

This implementation demonstrates:

1. **LangGraph Workflow**: StateGraph with conditional routing
2. **Agent Coordination**: Explicit A2A communication patterns
3. **MCP Protocol**: Standardized database access
4. **State Management**: Shared state across multiple agents
5. **Intent Classification**: Router-based query analysis
6. **Context Awareness**: Agents using information from other agents

## 🐛 Troubleshooting

### Database Not Found
```bash
python database_setup.py
```

### OpenAI API Errors
- Verify API key is set correctly
- Check account has credits
- Ensure network connection

### Import Errors
```bash
pip install -r requirements.txt --upgrade
```

### Notebook Kernel Issues
```bash
python -m ipykernel install --user --name=venv
```

## 📝 Assignment Compliance

This implementation satisfies all assignment requirements:

✅ **Part 1**: Three specialized agents (Router, Data, Support)
✅ **Part 2**: MCP server with 5 required tools + proper database schema
✅ **Part 3**: A2A coordination with all 3 scenarios
✅ **Test Scenarios**: All 5 required tests implemented
✅ **Deliverables**: Code repository, notebook, conclusion

## 🔮 Future Enhancements

- Add authentication and authorization
- Implement real-time MCP server with API endpoints
- Add caching for frequent queries
- Implement retry logic and circuit breakers
- Add comprehensive error handling
- Create web UI for system interaction
- Add monitoring and metrics dashboard
- Implement conversation history tracking

## 📚 References

- LangGraph Documentation: https://python.langchain.com/docs/langgraph
- Model Context Protocol: https://modelcontextprotocol.io
- Dr. Fouad Bousetouane's LangGraph Patterns (included in repository)

## 🤝 Contributing

This is an educational project. Feel free to extend and improve!

## 📄 License

MIT License - See LICENSE file for details

## 👨‍💻 Author

Implementation based on assignment requirements and LangGraph patterns by Dr. Fouad Bousetouane.

---

**Note**: This system is for educational purposes. For production use, implement proper security, error handling, and scalability measures.
