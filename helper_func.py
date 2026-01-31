def print_error(e: Exception, prefix: str = "Error") -> None:
    """Print any exception in a clean format."""
    return f"\n {prefix}: {e}"
