# learning functions in python - all list 
"""
pyutils.py — A collection of handy Python utility functions.
Just copy this file into your project and import what you need.
"""

import re
import os
import time
import unicodedata
import functools
from pathlib import Path
from datetime import datetime, date


# ---------- TEXT ----------

def slugify(text, separator="-"):
    """Convert text into a URL-friendly slug. e.g. 'Hello World!' -> 'hello-world'"""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", separator, text)


def truncate(text, max_length=100, suffix="..."):
    """Shorten text to max_length, breaking at the nearest word."""
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)].rsplit(" ", 1)[0] + suffix


def remove_extra_whitespace(text):
    """Collapse multiple spaces/tabs/newlines into single spaces."""
    return re.sub(r"\s+", " ", text).strip()


# ---------- DATES ----------

def format_date(value, output_format="%B %d, %Y", input_format="%Y-%m-%d"):
    """Format a date string, e.g. '2024-03-15' -> 'March 15, 2024'"""
    d = value if isinstance(value, (date, datetime)) else datetime.strptime(value, input_format)
    return d.strftime(output_format)


def days_between(start, end, fmt="%Y-%m-%d"):
    """Number of days between two date strings."""
    d1 = datetime.strptime(start, fmt)
    d2 = datetime.strptime(end, fmt)
    return (d2 - d1).days


def is_weekend(value, fmt="%Y-%m-%d"):
    """Check if a date string falls on Sat/Sun."""
    d = datetime.strptime(value, fmt)
    return d.weekday() >= 5


# ---------- FILES ----------

def list_files_by_extension(directory, extension):
    """List all files with a given extension in a directory (recursive)."""
    extension = extension.lstrip(".")
    return sorted(Path(directory).rglob(f"*.{extension}"))


def get_file_size_human(file_path):
    """Return human-readable file size, e.g. '4.2 MB'"""
    size = os.path.getsize(file_path)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024:
            return f"{size:.1f} {unit}" if unit != "B" else f"{size} {unit}"
        size /= 1024
    return f"{size:.1f} PB"


# ---------- DECORATORS ----------

def timer(func):
    """Print how long a function took to run."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.perf_counter() - start:.4f}s")
        return result
    return wrapper


def retry(max_attempts=3, delay=1.0, exceptions=Exception):
    """Retry a function if it raises an exception."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator


def memoize(func):
    """Cache function results based on arguments."""
    cache = {}
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    wrapper.cache_clear = cache.clear
    return wrapper


# ---------- VALIDATORS ----------

def is_valid_email(email):
    return bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email))


def is_valid_url(url):
    pattern = r"^https?://[^\s/$.?#].[^\s]*$"
    return bool(re.match(pattern, url))


def is_valid_phone(phone):
    return bool(re.match(r"^\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$", phone))


# ---------- QUICK DEMO ----------
if __name__ == "__main__":
    print(slugify("Hello, World! 2024"))
    print(truncate("This is a fairly long sentence to shorten", 20))
    print(format_date("2024-03-15"))
    print(is_valid_email("user@example.com"))

    @timer
    def slow_add(a, b):
        time.sleep(0.5)
        return a + b

    print(slow_add(2, 3))