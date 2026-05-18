"""📝 Structured Logger — No-Leak"""

import logging
from rich.logging import RichHandler

def get_logger(name: str) -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[RichHandler(rich_tracebacks=True, show_path=False)]
    )
    return logging.getLogger(name)

