from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging

from ...monitoring.endpoint import CheckResult

logger = logging.getLogger(__name__)


class AlertProvider(ABC):
    """Base class for all alert providers."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get("enabled", True)

    @abstractmethod
    async def send_alert(
        self, result: CheckResult, template: Optional[str] = None
    ) -> bool:
        """Send an alert for a failed health check."""
        pass

    def format_message(
        self, result: CheckResult, template: Optional[str] = None
    ) -> str:
        """Format an alert message using a template or default format."""
        if template:
            # Basic template substitution
            return template.format(
                endpoint_name=result.endpoint_name,
                url=result.url,
                status=result.status,
                message=result.message,
                status_code=result.status_code,
                response_time=f"{result.response_time:.2f}s",
                timestamp=result.timestamp.isoformat(),
                **result.details,
            )

        # Default format if no template provided
        timestamp = result.timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")

        message = (
            f"❌ Health check failed for {result.endpoint_name}\n"
            f"URL: {result.url}\n"
            f"Status: {result.status}\n"
            f"Message: {result.message}\n"
        )

        if result.status_code:
            message += f"Status code: {result.status_code}\n"

        message += f"Response time: {result.response_time:.2f}s\n"
        message += f"Time: {timestamp}\n"

        # Add selected details
        if result.details:
            message += "\nDetails:\n"
            for key, value in result.details.items():
                if isinstance(value, dict) and key in ["json_checks", "regex_checks"]:
                    message += f"- {key}:\n"
                    for check_name, check_result in value.items():
                        status = "✓" if check_result else "✗"
                        message += f"  - {check_name}: {status}\n"
                else:
                    message += f"- {key}: {value}\n"

        return message
