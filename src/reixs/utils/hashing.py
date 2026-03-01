"""Hashing utilities for source file integrity."""

import hashlib
from pathlib import Path


def compute_source_hash(filepath: Path) -> str:
    """Compute SHA-256 hash of a file's contents."""
    content = filepath.read_bytes()
    return hashlib.sha256(content).hexdigest()
