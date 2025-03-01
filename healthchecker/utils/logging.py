import logging
import sys
import json
from typing import Dict, Any
from datetime import datetime, timezone
import traceback


class JsonFormatter(logging.Formatter):
    """
    Formatter that outputs JSON strings with log information.
    """

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON string."""
        timestamp = datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat()

        # Create JSON dictionary with fields
        log_data = {
            "time": timestamp,
            "level": record.levelname,
            "name": record.name,
            "msg": record.getMessage(),
        }

        # Add exception info if present
        if record.exc_info:
            log_data["error"] = "".join(traceback.format_exception(*record.exc_info))

        return json.dumps(log_data)


class TextFormatter(logging.Formatter):
    """
    Formatter that outputs logs in structured key=value format.
    """

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as key=value pairs."""
        timestamp = datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat()

        # Start with fields
        parts = [
            f"time={timestamp}",
            f"level={record.levelname}",
            f"name={record.name}",
        ]

        parts.append(f'msg="{record.getMessage()}"')

        # Add exception info if present
        if record.exc_info:
            error = "\\n".join(
                line.rstrip()
                for line in "".join(
                    traceback.format_exception(*record.exc_info)
                ).splitlines()
            )
            parts.append(f'error="{error}"')

        return " ".join(parts)


def configure_logging(config: Dict[str, Any]) -> None:
    """
    Configure the logging system.

    Args:
        config: A dictionary containing:
            - level: The logging level (DEBUG, INFO, etc.)
            - format: The output format (json or text)
            - output: The output destination (stdout, stderr, or a file path)
    """
    log_level = getattr(logging, config.get("level", "INFO").upper())
    log_format = config.get("format", "json").lower()
    log_output = config.get("output", "stdout").lower()

    # Create a root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Clear existing handlers
    while root_logger.handlers:
        root_logger.removeHandler(root_logger.handlers[0])

    # Create handler based on output
    handler: logging.Handler
    if log_output == "stdout":
        handler = logging.StreamHandler(sys.stdout)
    elif log_output == "stderr":
        handler = logging.StreamHandler(sys.stderr)
    else:
        # Assume it's a file path
        handler = logging.FileHandler(log_output)

    # Set formatter based on format
    formatter: logging.Formatter
    if log_format == "json":
        formatter = JsonFormatter()
    else:
        formatter = TextFormatter()

    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
