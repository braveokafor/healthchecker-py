from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional, Deque
import asyncio
import aiohttp
import json
import logging
from collections import deque
from enum import Enum

from ..config.models import EndpointConfig

logger = logging.getLogger(__name__)


class HealthStatus(Enum):
    OK = "ok"
    CRITICAL = "critical"


class CheckResult:
    def __init__(
        self,
        endpoint_name: str,
        url: str,
        status: HealthStatus,
        response_time: float,
        status_code: Optional[int] = None,
        message: str = "",
        details: Optional[Dict[str, Any]] = None,
    ):
        self.endpoint_name = endpoint_name
        self.url = url
        self.status = status
        self.response_time = response_time
        self.status_code = status_code
        self.message = message
        self.details = details or {}
        self.timestamp = datetime.now(timezone.utc)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "endpoint_name": self.endpoint_name,
            "url": self.url,
            "status": self.status,
            "response_time": self.response_time,
            "status_code": self.status_code,
            "message": self.message,
            "details": self.details,
            "timestamp": self.timestamp.isoformat(),
        }


class EndpointChecker:
    """Handles health checking for a specific endpoint."""

    def __init__(self, config: EndpointConfig, session: Any):
        self.config = config
        self.session = session
        self.failure_history: Deque[datetime] = deque(
            maxlen=100
        )  # Store recent failures
        self.last_alert_time: Optional[datetime] = None

    async def check(self) -> CheckResult:
        """Perform a health check on the endpoint."""
        start_time = asyncio.get_event_loop().time()

        try:
            response = await self._make_request()
            response_time = asyncio.get_event_loop().time() - start_time

            # Check status code
            status_code_valid = self._validate_status_code(response.status)

            # Check response time
            time_valid = response_time <= self.config.response_time_threshold

            # Parse and check response body if needed
            body_valid, body_details = await self._validate_response_body(response)

            if status_code_valid and time_valid and body_valid:
                return CheckResult(
                    endpoint_name=self.config.name or "unknown",
                    url=self.config.url,
                    status=HealthStatus.OK,
                    response_time=response_time,
                    status_code=response.status,
                    message="Health check passed",
                    details={"body_checks": body_details},
                )
            else:
                # Construct failure details
                details = {
                    "status_code_valid": status_code_valid,
                    "response_time_valid": time_valid,
                    "body_valid": body_valid,
                    "body_details": body_details,
                }

                failure = CheckResult(
                    endpoint_name=self.config.name or "unknown",
                    url=self.config.url,
                    status=HealthStatus.CRITICAL,
                    response_time=response_time,
                    status_code=response.status,
                    message=self._get_failure_message(
                        status_code_valid, time_valid, body_valid
                    ),
                    details=details,
                )

                self._record_failure(failure)
                return failure

        except asyncio.TimeoutError:
            response_time = asyncio.get_event_loop().time() - start_time
            failure = CheckResult(
                endpoint_name=self.config.name or "unknown",
                url=self.config.url,
                status=HealthStatus.CRITICAL,
                response_time=response_time,
                message=f"Request timed out after {self.config.timeout} seconds",
                details={"error": "timeout"},
            )
            self._record_failure(failure)
            return failure

        except Exception as e:
            response_time = asyncio.get_event_loop().time() - start_time
            failure = CheckResult(
                endpoint_name=self.config.name or "unknown",
                url=self.config.url,
                status=HealthStatus.CRITICAL,
                response_time=response_time,
                message=f"Error performing health check: {str(e)}",
                details={"error": str(e), "error_type": e.__class__.__name__},
            )
            self._record_failure(failure)
            return failure

    async def _make_request(self):
        """Make an HTTP request to the endpoint."""
        method = self.config.method.lower()
        url = self.config.url
        headers = self.config.headers
        body = self.config.body
        timeout = aiohttp.ClientTimeout(total=self.config.timeout)

        request_kwargs = {"headers": headers, "timeout": timeout}

        # Add request body if specified
        if body:
            if isinstance(body, dict):
                request_kwargs["json"] = body
            else:
                request_kwargs["data"] = body

        # Get the appropriate request method from the session
        request_method = getattr(self.session, method)

        # Execute the request with the retry policy
        retry_config = self.config.retry
        for attempt in range(retry_config.attempts):
            try:
                return await request_method(url, **request_kwargs)
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                # Last attempt, re-raise the exception
                if attempt == retry_config.attempts - 1:
                    raise

                # Calculate backoff delay
                delay = retry_config.backoff_factor * (2**attempt)
                logger.debug(
                    f"Request to {url} failed, retrying in {delay:.2f}s: {str(e)}"
                )
                await asyncio.sleep(delay)

    def _validate_status_code(self, status_code: int) -> bool:
        """Validate the HTTP status code against expected codes and ranges."""
        # Check exact status codes
        if status_code in self.config.expected_status_codes:
            return True

        # Check status code ranges
        for range_str in self.config.expected_status_ranges:
            start, end = map(int, range_str.split("-"))
            if start <= status_code <= end:
                return True

        return False

    async def _validate_response_body(self, response) -> tuple[bool, Dict[str, Any]]:
        """Validate the response body against JSON path and regex checks."""
        details: Dict[str, Any] = {}

        # Skip body validation if no checks configured
        if not self.config.json_path_checks and not self.config.regex_checks:
            return True, details

        try:
            # Read response body
            body_text = await response.text()

            # Check JSON path expressions if configured
            if self.config.json_path_checks:
                json_check_results = {}
                try:
                    body_json = await response.json()
                    # Import here to avoid circular imports
                    from .response_parser import validate_json_paths

                    json_check_results = validate_json_paths(
                        body_json, self.config.json_path_checks
                    )
                    details["json_checks"] = json_check_results
                    if not all(json_check_results.values()):
                        return False, details
                except (json.JSONDecodeError, ValueError):
                    # JSON parsing failed
                    details["json_parse_error"] = {
                        "message": "Failed to parse response as JSON"
                    }
                    if self.config.json_path_checks:
                        # If JSON checks are required but parsing failed
                        return False, details

            # Check regex patterns if configured
            if self.config.regex_checks:
                # Import here to avoid circular imports
                from .response_parser import validate_regex_patterns

                regex_check_results = validate_regex_patterns(
                    body_text, self.config.regex_checks
                )
                details["regex_checks"] = regex_check_results
                if not all(regex_check_results.values()):
                    return False, details

            return True, details

        except Exception as e:
            logger.error(f"Error validating response body: {str(e)}")
            details["error"] = {"message": f"Body validation error: {str(e)}"}
            return False, details

    def _record_failure(self, result: CheckResult):
        """Record a health check failure for alert threshold calculation."""
        current_time = datetime.now(timezone.utc)
        self.failure_history.append(current_time)

        # Check if we need to trigger an alert based on failure threshold
        relevant_window = current_time - timedelta(seconds=self.config.failure_window)
        recent_failures = [t for t in self.failure_history if t >= relevant_window]

        if len(recent_failures) >= self.config.failure_threshold:
            # Mark as needing an alert
            result.details["alert_required"] = True
            result.details["failure_count"] = len(recent_failures)
            result.details["failure_window"] = f"{self.config.failure_window}s"

    def _get_failure_message(
        self, status_code_valid: bool, time_valid: bool, body_valid: bool
    ) -> str:
        """Generate a failure message based on the type of failure."""
        messages = []

        if not status_code_valid:
            messages.append("Unexpected status code")

        if not time_valid:
            messages.append(
                f"Response time exceeded threshold of {self.config.response_time_threshold}s"
            )

        if not body_valid:
            messages.append("Response body validation failed")

        return ", ".join(messages) if messages else "Health check failed"
