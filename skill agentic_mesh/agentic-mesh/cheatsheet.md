# Cheatsheet & Decision Layer: Agentic Mesh

Compact decision tables, rules of thumb, thresholds, and operational heuristics from *Agentic Mesh* by Eric Broda & Davis Broda.

---

## 1. Core Decision Rules

- **Workflow vs. Agent Decision Rule**:
  - *IF* the process has a known, fixed sequence of steps and predictable inputs -> **Use an AI Workflow** (Prompt Chain, Router, or Orchestrator).
  - *IF* the process involves ambiguity, unexpected obstacles, dynamic tool discovery, or open-ended goals -> **Use an Autonomous Agent**.
- **Microagent Boundary Rule**:
  - *IF* an agent requires more than 7–10 distinct tools or spans multiple business domains -> **Decompose into multiple Microagents** coordinated by a Fleet Leader.
- **Communication Protocol Decision Rule**:
  - *IF* the operation is a low-latency, read-only data lookup (< 500ms) -> **Use Synchronous gRPC / HTTP**.
  - *IF* the operation involves multi-agent coordination, long-running tasks, or mission state changes -> **Use Asynchronous Event-Driven Messaging (Kafka/Pub-Sub)**.
- **Human-in-the-Loop (HITL) Threshold Rule**:
  - *IF* an action is irreversible, exceeds financial spending thresholds, touches production database schemas, or alters customer contracts -> **Enforce Tier 3 Pre-Execution Human Approval Gate**.
  - *ELSE* -> **Run Fully Autonomous (Tier 1) with Post-Hoc Audit Notification (Tier 2)**.

---

## 2. Decision Tree: Multi-Agent Architecture Selection

```
Need to automate a business process with AI?
│
├── Are the steps, data paths, and outputs 100% predictable?
│   ├── YES ──► Implement an AI WORKFLOW (Anthropic Chaining/Routing)
│   └── NO  ──► Implement an AUTONOMOUS AGENT
│
Does the task exceed the scope of a single specialist domain?
│
├── NO  ──► Implement a single SPECIALIST MICROAGENT (Docker/K8s + mTLS)
└── YES ──► Assemble an AGENT FLEET
            │
            ├── Need strict, auditable, multi-stage delegation?
            │   └──► Use HIERARCHICAL FLEET (Fleet Leader + Specialists)
            │
            ├── Need distributed exploration or sensor data processing?
            │   └──► Use SWARM / PEER-TO-PEER FLEET (Shared Workspace)
            │
            └── Spanning multiple business units or enterprise boundaries?
                └──► Use FEDERATED FLEET (Agentic Mesh Registry + Event Mesh)
```

---

## 3. Trade-off Matrix: Communication & Architecture Options

| Architecture Option | Strengths | Weaknesses | Best Fit |
| :--- | :--- | :--- | :--- |
| **Monolithic Agent** | Rapid prototyping, zero network hops | High context pollution, brittle, untraceable | Hackathons, 1-day POCs |
| **Synchronous REST / gRPC** | Low latency, simple mental model | Cascading timeouts, tight temporal coupling | Fast database/read tool lookups |
| **Event-Driven Messaging** | Infinite scale, resilient, event replay | Higher infrastructure overhead, eventual consistency | Fleet collaboration, long-running tasks |
| **Shared Workspace (Blackboard)** | Unified super-context, decoupled communication | Requires shared persistent state store | Complex multi-agent investigations |
| **Hierarchical Fleet** | Clear accountability, auditable delegation | Fleet Leader can become a cognitive bottleneck | Complex enterprise mission workflows |
| **Swarm / P2P Fleet** | Highly resilient, no single point of failure | Harder to debug, risk of convergence delays | Market simulation, distributed sensing |

---

## 4. Operational Thresholds & Defaults

- **Reliability Target**: Aim for individual microagent step accuracy $> 99\%$; compound accuracy drops exponentially ($0.95^{10} \approx 60\%$, but $0.99^{10} \approx 90.4\%$).
- **Context Window Utilization**: Keep working system prompts and tools under 30% of total model context to prevent attention degradation and lost-in-the-middle phenomena.
- **Maximum Agent Conversation Turns**: Hard-cap inter-agent conversation loops at **10 to 15 turns** before forcing termination or human escalation.
- **Ephemeral Credential Lifetime**: Microagent OAuth/SPIFFE tokens should expire within **5 to 15 minutes**.
- **Mission Cost Budget**: Define hard maximum token expenditure per mission (e.g., max $1.50 per customer support resolution); abort and alert if exceeded.
- **Recertification Cadence**: Microagents in the Registry must undergo automated regression and safety recertification every **30 to 90 days** or upon any model weight update.

---

## 5. Tells & Smells (Warning Signs & Heuristics)

- **The "God Agent" Smell**: If an agent prompt contains > 2,000 words of instructions explaining 15 different job responsibilities, you are building a monolith that will fail in production. Decompose into microagents.
- **The "Infinite Loop" Tell**: If token usage climbs linearly while no tool calls or state updates are emitted, the agent is stuck in an ungrounded reasoning loop. Implement turn limits and watchdog timers.
- **The "Silent Drift" Smell**: If the business team reports that an agent's tone or recommendations subtly changed without any code deployment, an upstream foundation model provider updated their API model weights. Pin exact model versions.
- **The "Alert Fatigue" Tell**: If human reviewers are approving 100% of HITL requests in under 2 seconds, your approval thresholds are too low. Automate the low-risk items and reserve HITL for genuine risk.
