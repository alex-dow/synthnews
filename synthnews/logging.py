"""Colored console logging for synthnews using colorlog. File output stays plain."""

import logging
import sys
from pathlib import Path

import colorlog

LOGGER = logging.getLogger("synth_news")

_CONSOLE_FMT = "%(asctime)s | %(log_color)s%(levelname)-7s%(reset)s | %(message)s"
_FILE_FMT = "%(asctime)s | %(levelname)-7s | %(message)s"

_LOG_COLORS = {
    "DEBUG": "cyan",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "bold_red",
}


def configure_logging(log_file: Path | None, verbose: bool) -> None:
    """Configure the synth_news logger: colored console and optional plain file."""
    LOGGER.setLevel(logging.DEBUG)
    LOGGER.handlers.clear()
    LOGGER.propagate = False

    console_handler = colorlog.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    console_handler.setFormatter(
        colorlog.ColoredFormatter(
            _CONSOLE_FMT,
            log_colors=_LOG_COLORS,
            datefmt=None,
            reset=True,
        )
    )
    LOGGER.addHandler(console_handler)

    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(_FILE_FMT))
        LOGGER.addHandler(file_handler)
