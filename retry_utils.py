#!/usr/bin/env python3
"""
Retry utilities with exponential backoff for handling transient failures.
"""

import time
import random
from functools import wraps
from typing import Callable, Type, Tuple, Any


def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
):
    """
    Retry decorator with exponential backoff and optional jitter.
    
    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        exponential_base: Base for exponential backoff
        jitter: Whether to add random jitter to delay
        exceptions: Tuple of exceptions to catch and retry on
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(max_retries + 1):  # +1 for initial attempt
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt == max_retries:  # Last attempt exhausted
                        break
                    
                    # Calculate delay with exponential backoff
                    delay = min(
                        base_delay * (exponential_base ** attempt),
                        max_delay
                    )
                    
                    # Add jitter if enabled (±25% randomness)
                    if jitter:
                        delay *= random.uniform(0.75, 1.25)
                    
                    # Log the retry attempt
                    print(f"   ⚠️  Attempt {attempt + 1} failed: {e}. Retrying in {delay:.2f}s...")
                    time.sleep(delay)
            
            # If we got here, all retries exhausted
            raise last_exception
        
        return wrapper
    return decorator


# Convenience decorators for common use cases
def retry_mongodb(max_retries: int = 3, base_delay: float = 1.0):
    """Retry decorator for MongoDB operations."""
    from pymongo.errors import (
        AutoReconnect, 
        NetworkTimeout, 
        ServerSelectionTimeoutError,
        ConnectionFailure
    )
    return retry_with_backoff(
        max_retries=max_retries,
        base_delay=base_delay,
        exceptions=(
            AutoReconnect, 
            NetworkTimeout, 
            ServerSelectionTimeoutError,
            ConnectionFailure,
            Exception  # Catch-all for safety
        )
    )


def retry_github_api(max_retries: int = 3, base_delay: float = 1.0):
    """Retry decorator for GitHub API calls."""
    import requests
    return retry_with_backoff(
        max_retries=max_retries,
        base_delay=base_delay,
        exceptions=(
            requests.exceptions.RequestException,
            Exception  # Catch-all for safety
        )
    )


def retry_subprocess(max_retries: int = 2, base_delay: float = 0.5):
    """Retry decorator for subprocess calls."""
    import subprocess
    return retry_with_backoff(
        max_retries=max_retries,
        base_delay=base_delay,
        exceptions=(
            subprocess.SubprocessError,
            Exception  # Catch-all for safety
        )
    )