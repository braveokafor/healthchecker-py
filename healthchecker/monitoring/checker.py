import asyncio
import logging
import time
from typing import Dict, Optional
import aiohttp

from ..config.models import AppConfig
from .endpoint import EndpointChecker, CheckResult, HealthStatus
from ..alerting.manager import AlertManager

logger = logging.getLogger(__name__)


class MonitoringManager:
    """Manages the health check monitoring system."""

    def __init__(self, config: AppConfig, alert_manager: AlertManager):
        self.config = config
        self.alert_manager = alert_manager
        self.checkers: Dict[str, EndpointChecker] = {}
        self.session: Optional[aiohttp.ClientSession] = None
        self.running = False
        self.check_results: Dict[str, CheckResult] = {}
        self.semaphore = asyncio.Semaphore(config.concurrency_limit)

    async def start(self):
        """Start the monitoring system."""
        if self.running:
            logger.warning("Monitoring system is already running")
            return

        logger.info("Starting health check monitoring system")
        self.running = True

        # Create HTTP session
        timeout = aiohttp.ClientTimeout(total=60)  # Default max timeout
        self.session = aiohttp.ClientSession(timeout=timeout)

        # Create checkers for all endpoints
        for endpoint_config in self.config.endpoints:
            self.checkers[endpoint_config.name] = EndpointChecker(
                config=endpoint_config, session=self.session
            )

        # Start the monitoring tasks
        try:
            await self._monitor_all_endpoints()
        finally:
            await self.stop()

    async def stop(self):
        """Stop the monitoring system."""
        if not self.running:
            return

        logger.info("Stopping health check monitoring system")
        self.running = False

        # Close HTTP session
        if self.session:
            await self.session.close()
            self.session = None

    async def _monitor_all_endpoints(self):
        """Start monitoring tasks for all endpoints."""
        tasks = []

        for name, checker in self.checkers.items():
            task = asyncio.create_task(self._monitor_endpoint(name, checker))
            tasks.append(task)

        # Run all monitoring tasks
        await asyncio.gather(*tasks, return_exceptions=True)

    async def _monitor_endpoint(self, name: str, checker: EndpointChecker):
        """Continuously monitor a single endpoint."""
        logger.info(f"Starting monitoring for endpoint: {name}")

        while self.running:
            start_time = time.time()

            try:
                # Use semaphore to limit concurrent requests
                async with self.semaphore:
                    result = await checker.check()

                # Store the result
                self.check_results[name] = result

                # Log the result
                if result.status == HealthStatus.OK:
                    logger.info(
                        f"Health check for {name} succeeded: {result.response_time:.2f}s"
                    )
                else:
                    logger.warning(f"Health check for {name} failed: {result.message}")

                # Send alert if needed
                if result.status != HealthStatus.OK and result.details.get(
                    "alert_required", False
                ):
                    await self.alert_manager.send_alert(result)

            except Exception as e:
                logger.error(f"Error monitoring endpoint {name}: {str(e)}")

            # Calculate time to wait until next check
            elapsed = time.time() - start_time
            wait_time = max(0.1, checker.config.interval - elapsed)

            # Wait until next check
            await asyncio.sleep(wait_time)
