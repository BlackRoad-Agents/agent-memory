# agent-memory

Persistent memory system for BlackRoad agents. SQLite-backed with full-text search.

## Usage

```python
from memory import AgentMemory

mem = AgentMemory()

# Save memories
mem.save("road", "personality", "helpful fleet coordinator")
mem.save("road", "last_task", "deployed 3 workers to Octavia")

# Retrieve
mem.get("road", "personality")          # "helpful fleet coordinator"
mem.get_all("road")                     # {key: value, ...}
mem.get_recent("road", 5)              # last 5 memories

# Full-text search
mem.search("road", "deploy workers")   # FTS5 ranked results
```

## CLI

```bash
python memory.py <agent_id> save <key> <value>
python memory.py <agent_id> get <key>
python memory.py <agent_id> all
python memory.py <agent_id> search <query>
python memory.py <agent_id> recent [n]
```

## Storage

Creates `agent_memory.db` (SQLite) in the current directory. Override with `AGENT_MEMORY_DB` env var.

Uses FTS5 virtual tables for fast full-text search with automatic index triggers.

## Part of BlackRoad-Agents

Remember the Road. Pave Tomorrow.

BlackRoad OS, Inc. — Incorporated 2025.
