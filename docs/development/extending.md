# Extending the System

Health Check Monitor is designed to be easily extended. This section covers how to add new capabilities.

## Adding a New Alert Provider

1. Create a new provider class in `healthchecker/alerting/providers/`:

```python
from typing import Dict, Any, Optional
from .base import AlertProvider
from ...monitoring.endpoint import CheckResult

class NewProvider(AlertProvider):
    """New alert provider implementation."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        # Initialise provider-specific settings
        self.api_key = config.get("api_key")
        self.endpoint = config.get("endpoint")
        
    async def send_alert(self, result: CheckResult, template: Optional[str] = None) -> bool:
        """Send an alert via the new provider."""
        if not self.enabled:
            return False
            
        try:
            # Format the message
            message = self.format_message(result, template)
            
            # Provider-specific logic to send alert
            # ...
            
            return True
        except Exception as e:
            logger.error(f"Error sending alert: {str(e)}")
            return False
```

2. Register your provider in `alerting/manager.py`:

```python
class AlertManager:
    """Manages alert delivery and rate limiting."""
    
    # Registry of available alert providers
    PROVIDERS = {
        "slack": SlackProvider,
        "email": EmailProvider,
        "new_provider": NewProvider  # Add your provider here
    }
```

3. Update the configuration schema to support your new provider.

## Adding Response Validation Methods

To add new response validation methods:

1. Extend the `response_parser.py` file with your new validation logic
2. Update the configuration schema to include your new validation options
3. Add validation processing in the endpoint checker

## Creating Custom Commands

To add new command line options:

1. Update the CLI parser in `cli.py`
2. Implement the handler for your new command
3. Update documentation to reflect the new functionality

The modular architecture makes it easy to extend the system without modifying existing code.