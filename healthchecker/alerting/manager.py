import logging
from typing import Dict, List
from datetime import datetime, timedelta, timezone

from ..config.models import AlertConfig
from ..monitoring.endpoint import CheckResult
from .providers.base import AlertProvider
from .providers.email import EmailProvider

logger = logging.getLogger(__name__)


class AlertManager:
    """Manages alert delivery and rate limiting."""

    # Registry of available alert providers
    PROVIDERS = {"email": EmailProvider}

    def __init__(self, config: AlertConfig, mock_mode: bool = False):
        self.config = config
        self.mock_mode = mock_mode
        self.providers: Dict[str, AlertProvider] = {}
        self.alert_history: Dict[str, List[datetime]] = (
            {}
        )  # Endpoint name -> alert times
        self._initialize_providers()

    def _initialize_providers(self):
        """Initialize all configured alert providers."""
        for name, provider_config in self.config.providers.items():
            if not provider_config.enabled:
                logger.info(f"Alert provider '{name}' is disabled")
                continue

            provider_class = self.PROVIDERS.get(provider_config.type)
            if not provider_class:
                logger.error(f"Unknown alert provider type: {provider_config.type}")
                continue

            try:
                self.providers[name] = provider_class(provider_config.config)
                logger.info(
                    f"Initialized alert provider: {name} ({provider_config.type})"
                )
            except Exception as e:
                logger.error(f"Error initializing alert provider '{name}': {str(e)}")

    def _should_send_alert(self, endpoint_name: str) -> bool:
        """
        Check if we should send an alert based on rate limiting rules.

        Args:
            endpoint_name: The name of the endpoint

        Returns:
            True if an alert should be sent, False otherwise
        """
        # If no history for this endpoint, always allow
        if endpoint_name not in self.alert_history:
            return True

        # Get alert history for this endpoint
        history = self.alert_history[endpoint_name]

        # Check cooldown period
        if history:
            last_alert_time = history[-1]
            cooldown_end = last_alert_time + timedelta(
                seconds=self.config.cooldown_period
            )
            if datetime.now(timezone.utc) < cooldown_end:
                return False

        # Check hourly rate limit
        one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
        recent_alerts = [t for t in history if t > one_hour_ago]

        return len(recent_alerts) < self.config.max_alerts_per_hour

    def _record_alert(self, endpoint_name: str) -> None:
        """
        Record an alert attempt in the history.

        Args:
            endpoint_name: The name of the endpoint
        """
        if endpoint_name not in self.alert_history:
            self.alert_history[endpoint_name] = []

        self.alert_history[endpoint_name].append(datetime.now(timezone.utc))

        # Cleanup old history (older than 24 hours)
        cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
        self.alert_history[endpoint_name] = [
            t for t in self.alert_history[endpoint_name] if t > cutoff
        ]

    async def send_alert(self, result: CheckResult) -> bool:
        """Send an alert for a failed health check."""
        endpoint_name = result.endpoint_name

        # Check if we should alert based on rate limiting
        if not self._should_send_alert(endpoint_name):
            logger.info(f"Alert for {endpoint_name} suppressed due to rate limiting")
            return False

        # Record this alert attempt
        self._record_alert(endpoint_name)

        # In mock mode, just log instead of sending
        if self.mock_mode:
            logger.info(f"MOCK ALERT for {endpoint_name}: {result.message}")
            return True

        # Get the appropriate template if available
        template = self.config.templates.get(result.status.value)

        # Send to all enabled providers
        success = False
        for name, provider in self.providers.items():
            if provider.enabled:
                try:
                    provider_success = await provider.send_alert(result, template)
                    success = success or provider_success
                except Exception as e:
                    logger.error(f"Error sending alert via provider '{name}': {str(e)}")

        return success
