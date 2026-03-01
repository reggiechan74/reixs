"""Known REIXS task types."""

KNOWN_TASK_TYPES = {
    "lease abstraction",
    "lease_abstraction",
}


def is_known_task_type(task_type: str) -> bool:
    return task_type.lower().strip() in KNOWN_TASK_TYPES
