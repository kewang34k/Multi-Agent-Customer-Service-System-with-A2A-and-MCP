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

The notebook provides a complete walkthrough with detailed explanations and outputs.

1. Start Jupyter:
```bash
jupyter notebook
```

2. Open `Multi_Agent_Customer_Service_Complete.ipynb`

3. Run all cells sequentially to see:
   - **Part 1-2**: Setup and database initialization
   - **Part 3**: MCP Server with 5 tools
   - **Part 4-5**: Agent implementations (Router, Data, Support)
   - **Part 6**: LangGraph workflow compilation
   - **Part 7**: Three coordination scenarios with A2A logs
   - **Part 8**: Five required test scenarios
   - **Part 9**: System statistics and analysis
   - **Conclusion**: Learning outcomes and challenges
   - **Improvement**: Router agent refinement and verification tests

4. Each scenario shows:
   - Agent execution flow
   - MCP tool calls
   - A2A communication logs
   - Final responses

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

### Pattern 1: Task Allocation (Simple Routing)
Router analyzes query and delegates to single specialist agent.

**Flow:**
```
Router → [Analyze Intent] → Data Agent → Synthesize → Response
```

**Example Query:** "Get customer information for ID 5"

**A2A Communication Log:**
```
[ROUTER] Analyzed query - Intent: account_info
[ROUTER → DATA] Requesting customer data
[DATA] Calling MCP: get_customer_history(5)
[DATA → ROUTER] Retrieved customer context
[ROUTER] Finalized response
```

**Use Case**: Simple data retrieval queries where one agent can handle the entire request.

### Pattern 2: Negotiation/Coordination (Multi-Agent)
Multiple agents coordinate when query requires both data context and support expertise.

**Flow:**
```
Router → Data Agent → [Share Context] → Support Agent → Synthesize → Response
```

**Example Query:** "I'm customer 1 and need help upgrading my account"

**A2A Communication Log:**
```
[ROUTER] Analyzed query - Intent: account_info
[ROUTER → DATA] Requesting customer data
[ROUTER → SUPPORT] Routing to support agent
[DATA] Calling MCP: get_customer_history(1)
[DATA → SUPPORT] Providing customer context for Alice Johnson
[SUPPORT] Using customer context from Data Agent
[SUPPORT → ROUTER] Generated response
[ROUTER] Finalized response
```

**Use Case**: Queries needing customer context + personalized support (account help, billing questions, technical issues).

### Pattern 3: Multi-Step Coordination (Complex Decomposition)
Complex queries decomposed into sequential sub-tasks with intermediate processing.

**Flow:**
```
Router → [Decompose] → Data (Step 1) → Data (Step 2) → ... → Synthesize Report
```

**Example Query:** "Show me all active customers who have open tickets"

**A2A Communication Log:**
```
[ROUTER] Decomposing complex query into sub-tasks
[ROUTER → DATA] Step 1: Get all active customers
[DATA → ROUTER] Found 5 active customers
[ROUTER → DATA] Step 2: Check tickets for each customer
[DATA → ROUTER] Found 4 customers with open tickets
[ROUTER] Step 3: Formatting report
[ROUTER] Multi-step coordination complete
```

**Use Case**: Complex analytical queries requiring multiple database operations and data aggregation.

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

## 🎓 Key Learnings & Implementation Insights

### What This Implementation Teaches

1. **State Management is Critical**: Using LangGraph's StateGraph pattern allows agents to share context seamlessly while maintaining clean separation of concerns. The shared state enables complex workflows without tight coupling between agents.

2. **A2A Coordination Requires Explicit Logging**: Agent-to-Agent communication isn't just about passing data—it's about understanding how agents collaborate. The A2A logging system (`a2a_log`) tracks every handoff and decision, making the system transparent and debuggable.

3. **Router as Orchestrator**: The Router Agent makes critical decisions about which specialist agents to invoke and in what order. It analyzes intent, determines data requirements, and coordinates the workflow—acting as the "conductor" of the multi-agent orchestra.

4. **MCP Provides Clean Abstraction**: The Model Context Protocol creates a standardized interface for database access, allowing the Customer Data Agent to interact with data through well-defined tools without coupling to specific database implementations.

5. **Agent Negotiation for Complex Queries**: Multi-intent queries (like "cancel subscription with billing issues") require agents to coordinate and determine the best approach. This negotiation pattern is essential for real-world customer service scenarios.

### Technical Capabilities Demonstrated

- **LangGraph Workflow**: StateGraph with conditional routing and state persistence
- **Agent Coordination**: Three distinct A2A communication patterns
- **MCP Protocol**: 5 standardized tools for database operations
- **Intent Classification**: LLM-powered query analysis with fallback logic
- **Context Awareness**: Agents building on information from previous agents
- **Error Handling**: Robust JSON parsing with regex-based fallbacks

## 🚧 Challenges & Solutions

### Challenge 1: A2A Coordination Logging
**Problem**: Tracking agent-to-agent communications while maintaining clean workflow logic felt like adding unnecessary complexity.

**Solution**: Realized that A2A logging is essential for debugging and understanding system behavior. Implemented a simple list-based log (`a2a_log`) that gets passed through the state and appended by each agent. This provides complete visibility into the coordination flow.

### Challenge 2: Multi-Intent Query Handling
**Problem**: Queries like "cancel subscription with billing issues" require both billing context (Data Agent) and support guidance (Support Agent) with proper coordination.

**Solution**: Enhanced the Router Agent to detect multiple intents and determine if agents should run sequentially or in parallel. The router uses LLM-based analysis with fallback logic to ensure robust intent classification.

### Challenge 3: Conditional Routing in LangGraph
**Problem**: Determining when to route `Router → Data → Support` versus `Router → Support` based on whether customer context is needed.

**Solution**: Implemented conditional edges with explicit routing functions (`route_after_router`, `route_after_data`) that check state flags (`requires_data`, `requires_support`) to determine the next agent in the workflow.

### Challenge 4: Router Agent Reliability
**Problem**: Initial router implementation sometimes failed to request customer data even when a Customer ID was present in the query, leading to missed context.

**Solution**: Refined the router agent with:
- **Stricter system prompt** explicitly requiring data access when ID is present
- **Regex-based fallback** to extract Customer IDs if LLM parsing fails
- **Deterministic override** forcing `requires_data=true` when any Customer ID is detected
- **Robust JSON parsing** with cleanup logic to handle malformed LLM responses

### Challenge 5: Multi-Step Coordination
**Problem**: Complex queries like "find all active customers with open tickets" require breaking down into atomic MCP operations and synthesizing results.

**Solution**: Demonstrated decomposition pattern where the Router breaks complex queries into sub-tasks (Step 1: list customers, Step 2: check tickets for each, Step 3: format report), highlighting the importance of composable tools and clear agent responsibilities.

**Key Takeaway**: Multi-agent systems excel with complex queries, but require careful orchestration, explicit communication logging, and well-defined interfaces (like MCP) to maintain clarity and debuggability.

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
