import os
import pytest
import tempfile
import yaml

from healthchecker.config.models import (
    EndpointConfig,
    RetryConfig,
    AlertConfig,
)
from healthchecker.config.loader import load_config, resolve_env_vars


class TestConfigModels:
    """Test the Pydantic models for configuration validation."""

    def test_retry_config_defaults(self):
        """Test default values for RetryConfig."""
        config = RetryConfig()
        assert config.attempts == 3
        assert config.backoff_factor == 0.3

    def test_endpoint_config_validation(self):
        """Test validation of EndpointConfig."""
        # Basic config
        config = EndpointConfig(
            url="https://example.com/health", method="GET", expected_status_codes=[200]
        )
        assert config.name == "example.com"  # Auto-generated from URL

        # Invalid status range
        with pytest.raises(ValueError):
            EndpointConfig(
                url="https://example.com/health",
                expected_status_ranges=["200-600"],  # Invalid range
            )

    def test_alert_config_validation(self):
        """Test alert config validation."""
        config = AlertConfig(
            providers={
                "slack": {
                    "type": "slack",
                    "config": {"webhook_url": "https://hooks.slack.com/test"},
                }
            },
            cooldown_period=300.0,
            max_alerts_per_hour=5,
        )

        assert config.cooldown_period == 300.0
        assert config.max_alerts_per_hour == 5


class TestConfigLoader:
    """Test the configuration loader functionality."""

    def test_env_var_resolution(self):
        """Test resolution of environment variables in strings."""
        os.environ["TEST_API_KEY"] = "secret123"

        # Basic variable
        result = resolve_env_vars("Bearer ${TEST_API_KEY}")
        assert result == "Bearer secret123"

        # Variable with default
        result = resolve_env_vars("Bearer ${MISSING_VAR:-default_key}")
        assert result == "Bearer default_key"

    def test_load_config(self):
        """Test loading configuration."""
        config_data = {
            "endpoints": [
                {
                    "url": "https://example.com/api",
                }
            ],
            "alerting": {
                "providers": {"slack": {"type": "slack", "config": {}}},
                "cooldown_period": 300.0,
                "max_alerts_per_hour": 5,
            },
        }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False
        ) as temp:
            yaml.dump(config_data, temp)

        try:
            # Load the config
            config = load_config(temp.name)

            # Verify loaded config
            assert len(config.endpoints) == 1
            assert config.alerting.cooldown_period == 300.0
            assert config.alerting.max_alerts_per_hour == 5

        finally:
            os.unlink(temp.name)
