import traceback


def print_error(
    e: Exception, prefix: str = "Error", show_traceback: bool = True
) -> None:
    """Print any exception in a clean format."""
    print(f"\n {prefix}: {e}")
    if show_traceback:
        traceback.print_exc()
    return
