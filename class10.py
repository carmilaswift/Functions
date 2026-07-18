"""
quicktools.py — Everyday utility functions for common small tasks.
Copy this into a file and run directly, or import individual functions.
"""

import json
import random
import string
import hashlib
import secrets
from datetime import datetime


# ---------- PASSWORDS & SECURITY ----------

def generate_password(length=16, use_symbols=True):
    """Generate a secure random password."""
    chars = string.ascii_letters + string.digits
    if use_symbols:
        chars += "!@#$%^&*()-_=+"
    return "".join(secrets.choice(chars) for _ in range(length))


def hash_text(text, algorithm="sha256"):
    """Return a hex hash of the given text (sha256, md5, sha1, etc.)"""
    h = hashlib.new(algorithm)
    h.update(text.encode("utf-8"))
    return h.hexdigest()


def generate_id(length=8):
    """Generate a short random alphanumeric ID, e.g. for filenames or keys."""
    chars = string.ascii_lowercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))


# ---------- UNIT CONVERSION ----------

def celsius_to_fahrenheit(c):
    return (c * 9 / 5) + 32


def fahrenheit_to_celsius(f):
    return (f - 32) * 5 / 9


def kg_to_lbs(kg):
    return kg * 2.20462


def lbs_to_kg(lbs):
    return lbs / 2.20462


def bytes_to_human(num_bytes):
    """Convert bytes to human-readable size, e.g. 1048576 -> '1.0 MB'"""
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if num_bytes < 1024:
            return f"{num_bytes:.1f} {unit}" if unit != "B" else f"{num_bytes} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f} PB"


# ---------- JSON / DATA ----------

def pretty_json(data):
    """Pretty-print a dict/list as indented JSON."""
    return json.dumps(data, indent=2, ensure_ascii=False)


def flatten_dict(d, parent_key="", sep="."):
    """
    Flatten a nested dictionary.
    e.g. {"a": {"b": 1}} -> {"a.b": 1}
    """
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_dict(v, new_key, sep=sep))
        else:
            items[new_key] = v
    return items


def chunk_list(lst, size):
    """Split a list into chunks of a given size."""
    return [lst[i:i + size] for i in range(0, len(lst), size)]


# ---------- MISC ----------

def timestamp(fmt="%Y-%m-%d %H:%M:%S"):
    """Return the current timestamp as a formatted string."""
    return datetime.now().strftime(fmt)


def word_count(text):
    """Count words in a block of text."""
    return len(text.split())


def is_palindrome(text):
    """Check if a string is a palindrome, ignoring case and spaces."""
    cleaned = "".join(text.lower().split())
    return cleaned == cleaned[::-1]


def shuffle_string(text):
    """Return the characters of a string in random order."""
    chars = list(text)
    random.shuffle(chars)
    return "".join(chars)


# ---------- QUICK DEMO ----------
if __name__ == "__main__":
    print("Password:", generate_password())
    print("Hash:", hash_text("hello world"))
    print("Random ID:", generate_id())
    print("32°C in F:", celsius_to_fahrenheit(32))
    print("Bytes:", bytes_to_human(1048576))
    print("Timestamp:", timestamp())
    print("Palindrome check:", is_palindrome("A man a plan a canal Panama"))
    print("Chunked list:", chunk_list([1, 2, 3, 4, 5, 6, 7], 3))

    nested = {"user": {"name": "Alex", "address": {"city": "NYC"}}}
    print("Flattened:", flatten_dict(nested))
    print("Pretty JSON:\n", pretty_json(nested))