"""
B.A.D.I. Memory System

Provides both relational (SQLite) and vector (ChromaDB) storage
for conversations, tasks, preferences, and semantic search.
"""

from badi.memory.db import (
    init_db,
    get_db,
    get_or_create_user,
    save_interaction,
    save_task,
    update_task_status,
    get_recent_interactions,
    save_preference,
    get_preference,
    User,
    Preference,
    Interaction,
    Task,
    Memory
)

from badi.memory.vector_store import (
    get_vector_store,
    reload_vector_store,
    VectorStore
)

__all__ = [
    # Database functions
    "init_db",
    "get_db",
    "get_or_create_user",
    "save_interaction",
    "save_task",
    "update_task_status",
    "get_recent_interactions",
    "save_preference",
    "get_preference",
    # Database models
    "User",
    "Preference",
    "Interaction",
    "Task",
    "Memory",
    # Vector store
    "get_vector_store",
    "reload_vector_store",
    "VectorStore",
]
