import logging
import aiohttp
from typing import Dict, Any, Optional

from .base import AlertProvider
from ...monitoring.endpoint import CheckResult

logger = logging.getLogger(__name__)


class SlackProvider(AlertProvider):
    """Alert provider for Slack."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.webhook_url = config.get("webhook_url")
        self.channel = config.get("channel")
        self.username = config.get("username", "Health Monitor")
        self.icon_emoji = config.get("icon_emoji", ":warning:")

        if not self.webhook_url:
            logger.error("Slack webhook URL is required")
            self.enabled = False

    async def send_alert(
        self, result: CheckResult, template: Optional[str] = None
    ) -> bool:
        """Send an alert to Slack."""
        if not self.enabled or not self.webhook_url:
            return False

        try:
            # Format the message
            message = self.format_message(result, template)

            # Prepare the payload
            payload = {
                "text": message,
                "username": self.username,
                "icon_emoji": self.icon_emoji,
            }

            # Add channel if specified
            if self.channel:
                payload["channel"] = self.channel

            # Send the request
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.webhook_url, json=payload, timeout=10
                ) as response:
                    if response.status == 200:
                        logger.info(
                            f"Successfully sent Slack alert for {result.endpoint_name}"
                        )
                        return True
                    else:
                        content = await response.text()
                        logger.error(
                            f"Error sending Slack alert, status {response.status}: {content}"
                        )
                        return False

        except Exception as e:
            logger.error(f"Error sending Slack alert: {str(e)}")
            return False
