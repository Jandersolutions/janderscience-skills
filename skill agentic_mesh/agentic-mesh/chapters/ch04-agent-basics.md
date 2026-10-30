# Chapter 4: Agent Basics

## Core Idea
Autonomous agents mirror human organizational roles; understanding an agent requires analyzing its core physiological components—Brain, Memory, Tools, Task Management, and Context—and mapping individuals into teams (Fleets) and enterprises (Ecosystems).

## Frameworks Introduced
- **The Human-to-Agent Analogy Framework**:
  - Person -> Agent (Autonomous worker with specific skills and responsibilities)
  - Team -> Fleet (Specialized group collaborating toward a shared mission)
  - Enterprise -> Agentic Mesh (Federated organizational infrastructure providing governance, security, and communication)
- **The Seven Core Agent Capabilities**:
  1. *Task Planning*: Decomposing complex goals into sequential and parallel steps.
  2. *Task Execution*: Triggering APIs, executing scripts, and calling microservices.
  3. *Problem-Solving*: Identifying roadblocks, diagnosing errors, and replanning.
  4. *Tool Use*: Dynamically discovering and parameterizing external capabilities.
  5. *Memory and Context*: Retaining operational history across short-term and long-term storage.
  6. *Learning*: Updating behavioral priors based on feedback, evaluations, and few-shot examples.
  7. *Collaboration & Communication*: Exchanging structured messages with human operators and peer agents.

## Key Concepts
- **Agent Brain**: The cognitive processing engine (typically an LLM) responsible for intent recognition, reasoning, planning, and synthesis.
- **Short-Term Memory**: The active context window containing immediate instructions, conversation history, and tool call results.
- **Long-Term Memory**: External persistence stores (vector databases, relational stores, key-value caches) enabling semantic retrieval across sessions.
- **Context Engineering**: The deliberate architectural discipline of curating, formatting, pruning, and injecting relevant information into the prompt window.
- **Agent Tool**: An executable interface (REST API, database query, CLI command, MCP tool) that gives an agent agency in digital systems.
- **Replanning**: The ability of an agent to inspect a failed task execution, determine root cause, and formulate a new path forward.

## Mental Models
- **Think of Tools as an Agent's Hands**: The LLM brain can only think and output tokens; tools provide the physical hands to affect databases, codebases, and external systems.
- **Think of Context as Working Desk Space**: The LLM context window is finite desk space; cluttering it with irrelevant documents slows down cognition and causes hallucinations.

## Anti-patterns
- **Context Stuffing**: Dumping hundreds of pages of unindexed raw documentation into the prompt instead of using precise RAG and targeted tool queries.
- **Stateless Agent Operations**: Treating every agent interaction as a brand new session, forcing the agent to rediscover organizational context on every turn.
- **Unparameterized Tooling**: Providing agents with vague, ambiguous tool schemas lacking explicit data types, parameter descriptions, or failure modes.

## Reference Tables & Architecture
```
                  ┌─────────────────────────────────────────┐
                  │              AGENT "BRAIN"              │
                  │   (Foundation LLM / Cognitive Engine)   │
                  └────┬───────────────┬───────────────┬────┘
                       │               │               │
        ┌──────────────┴────┐   ┌──────┴──────┐  ┌─────┴───────────────┐
        │   TASK MANAGER    │   │   MEMORY    │  │ CONTEXT ENGINEERING │
        │ - Decomposing     │   │ - Short-Term│  │ - Dynamic RAG       │
        │ - Parameterizing  │   │ - Long-Term │  │ - Token Pruning     │
        │ - Replanning      │   │ - Episodic  │  │ - Tool Schemas      │
        └──────────────┬────┘   └─────────────┘  └─────────────────────┘
                       │
        ┌──────────────┴───────────────────────────────┐
        │               TOOL EXECUTION                 │
        │  [REST APIs]   [Database Queries]  [MCP Tools]│
        └──────────────────────────────────────────────┘
```

## Worked Example
An Agent tasked with: "Reconcile daily payments and report discrepancies":
1. *Task Planning*: Brain breaks goal into:
   - Step 1: Query payment gateway transactions for date range.
   - Step 2: Query bank ledger transactions.
   - Step 3: Run matching algorithm on transaction IDs and amounts.
   - Step 4: For unmatched rows, inspect gateway status codes.
   - Step 5: Draft reconciliation report and alert finance lead.
2. *Tool Use*: Agent calls `gateway_api.get_charges()` and `ledger_db.query()`.
3. *Problem-Solving*: Step 3 identifies a $450 discrepancy. Agent inspects gateway metadata, notices a delayed settlement code, and annotates the report with the exact root cause rather than raising a false alarm.

## Key Takeaways
1. An agent is much more than an LLM prompt: it is a software system comprising memory, context, tools, and execution controllers.
2. The human organization is the most effective mental model for structuring multi-agent architectures.
3. Context engineering is the primary determinant of agent reliability; managing token budgets and relevance is critical.
4. Agents must be equipped with replanning capabilities to handle unpredictable runtime environments.

## Connects To
- **Ch 3**: How agent components surpass static AI workflows.
- **Ch 5**: Translating these basics into enterprise microagent architectural patterns.
- **Ch 9 & 10**: Exposing agent tools and messaging across the Agentic Mesh.
