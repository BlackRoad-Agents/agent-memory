<!-- BlackRoad SEO Enhanced -->

# agent memory

> Part of **[BlackRoad OS](https://blackroad.io)** — Sovereign Computing for Everyone

[![BlackRoad OS](https://img.shields.io/badge/BlackRoad-OS-ff1d6c?style=for-the-badge)](https://blackroad.io)
[![BlackRoad-Agents](https://img.shields.io/badge/Org-BlackRoad-Agents-2979ff?style=for-the-badge)](https://github.com/BlackRoad-Agents)

**agent memory** is part of the **BlackRoad OS** ecosystem — a sovereign, distributed operating system built on edge computing, local AI, and mesh networking by **BlackRoad OS, Inc.**

### BlackRoad Ecosystem
| Org | Focus |
|---|---|
| [BlackRoad OS](https://github.com/BlackRoad-OS) | Core platform |
| [BlackRoad OS, Inc.](https://github.com/BlackRoad-OS-Inc) | Corporate |
| [BlackRoad AI](https://github.com/BlackRoad-AI) | AI/ML |
| [BlackRoad Hardware](https://github.com/BlackRoad-Hardware) | Edge hardware |
| [BlackRoad Security](https://github.com/BlackRoad-Security) | Cybersecurity |
| [BlackRoad Quantum](https://github.com/BlackRoad-Quantum) | Quantum computing |
| [BlackRoad Agents](https://github.com/BlackRoad-Agents) | AI agents |
| [BlackRoad Network](https://github.com/BlackRoad-Network) | Mesh networking |

**Website**: [blackroad.io](https://blackroad.io) | **Chat**: [chat.blackroad.io](https://chat.blackroad.io) | **Search**: [search.blackroad.io](https://search.blackroad.io)

---


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
