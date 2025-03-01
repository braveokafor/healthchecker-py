import logging

from ..config.models import AlertConfig
from ..monitoring.endpoint import CheckResult


logger = logging.getLogger(__name__)


class AlertManager:
    """Manages alert delivery and rate limiting."""

    def __init__(self, config: AlertConfig, mock_mode: bool = False):
        self.config = config
        self.mock_mode = mock_mode

    async def send_alert(self, result: CheckResult) -> bool:
        """Send an alert for a failed health check."""
        endpoint_name = result.endpoint_name

        # In mock mode, just log instead of sending
        logger.info(f"MOCK ALERT for {endpoint_name}: {result.message}")
        return True
