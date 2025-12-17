import json
import os

MEMORY_FILE = "agent_memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def update_memory(method: str, success: bool):
    memory = load_memory()
    if method not in memory:
        memory[method] = {"success": 0, "failure": 0}

    if success:
        memory[method]["success"] += 1
    else:
        memory[method]["failure"] += 1

    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)
