import os
import re
import yaml
from typing import Any
import logging

from .models import AppConfig

logger = logging.getLogger(__name__)

ENV_VAR_PATTERN = re.compile(r"\${([A-Za-z0-9_]+)(:-([^}]+))?}")


def resolve_env_vars(value: str) -> str:
    """Resolve environment variables in a string."""

    def _replace_env_var(match):
        env_var = match.group(1)
        default_value = match.group(3)

        if env_var in os.environ:
            return os.environ[env_var]
        elif default_value is not None:
            return default_value
        else:
            raise ValueError(
                f"Environment variable {env_var} not found and no default provided"
            )

    if isinstance(value, str):
        return ENV_VAR_PATTERN.sub(_replace_env_var, value)
    return value


def process_env_vars_recursive(config: Any) -> Any:
    """Process environment variables in config recursively."""
    if isinstance(config, dict):
        return {k: process_env_vars_recursive(v) for k, v in config.items()}
    elif isinstance(config, list):
        return [process_env_vars_recursive(item) for item in config]
    elif isinstance(config, str):
        return resolve_env_vars(config)
    else:
        return config


def load_config(config_path: str) -> AppConfig:
    """Load and validate configuration from YAML file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    try:
        with open(config_path, "r") as f:
            config_dict = yaml.safe_load(f)

        # Resolve environment variables
        config_dict = process_env_vars_recursive(config_dict)

        # Validate using Pydantic
        config = AppConfig.model_validate(config_dict)

        logger.info(f"Loaded configuration with {len(config.endpoints)} endpoints")
        return config

    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML config: {e}")
        raise
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        raise
