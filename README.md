# Health Check Monitor

A production-grade automated health monitoring system for web services built with Python and asyncio.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
[![Build Status][badge_build_status]][link_build_status]
[![Release Status][badge_release_status]][link_build_status]
[![Issues][badge_issues]][link_issues]
[![Pull Requests][badge_pulls]][link_pulls]

## Overview

Health Check Monitor helps you keep an eye on your web services by continuously checking their health status. Built with performance in mind, it can handle monitoring hundreds of endpoints simultaneously while using minimal resources.

### Key Features

- **Fast & Efficient** - Built on asyncio to monitor 1000+ endpoints without breaking a sweat
- **Smart Validation** - Check status codes, response times, JSON content, and regex patterns
- **Alert Management** - Configurable thresholds and cooldown periods to prevent alert fatigue
- **Multiple Notifications** - Send alerts to Slack, Email, or add your own channels
- **Battle-tested Reliability** - Built-in retries, circuit breakers, and self-healing
- **Easy Deployment** - Ready-to-use Docker image and `docker-compose.yaml` for quick setup

## Docker Quick Start

The fastest way to try Health Check Monitor:

1. Clone the repository:

```bash
git clone https://github.com/braveokafor/healthchecker-py.git
cd healthchecker-py
```

2. Run with docker-compose:

```bash
docker compose up
```

That's it! The monitoring system is now running with our example configuration.

3. See it in action:
   - Open [http://localhost:8025](http://localhost:8025) in your browser to access the MailHog UI
   - You'll see alert emails arriving as some test endpoints fail
   - The emails show information about why the endpoints are failing

4. Explore what's happening:
   - Check the example configuration at `examples/config.yaml` to see what's being monitored
   - View the docker-compose setup in `docker-compose.yaml` to understand the components
   - Look at container logs to see real-time monitoring output

When you're done exploring, press `Ctrl+C` or run `docker compose down` to stop all services.

## Standard Installation

### Prerequisites

- Python 3.9+
- pip

### From Source

```bash
git clone https://github.com/braveokafor/healthchecker-py.git
cd healthchecker-py
pip install -e .
```

### Using Docker

```bash
docker pull ghcr.io/braveokafor/healthchecker-py:latest
```

## Configuration Quick Start

1. Create a `config.yaml` file:

```yaml
# Basic config.yaml
endpoints:
  - name: api-health
    url: https://httpbin.org/status/200
    method: GET
    expected_status_codes: [200]
    response_time_threshold: 3.0
    interval: 60.0

alerting:
  providers:
    email:
      type: email
      enabled: true
      config:
        smtp_server: localhost
        smtp_port: 1025
        from_address: "monitor@example.com"
        to_addresses:
          - "admin@example.com"
  
  cooldown_period: 300.0
  max_alerts_per_hour: 10

logging:
  level: INFO
  format: json
  output: stdout

concurrency_limit: 10
```

2. Start monitoring:

```bash
healthcheck-monitor --config config.yaml --mock-alerts
```

## Configuration Guide

Your configuration file is the heart of the system. Here's how to set it up:

### Monitoring Endpoints

Define what services you want to monitor:

```yaml
endpoints:
  - name: SUCCESS-httpbin-status                # Simple status check
    url: https://httpbin.org/status/200
    method: GET
    expected_status_codes: [200]
    response_time_threshold: 3.0
    timeout: 5.0
    interval: 60.0
    retry:
      attempts: 3
      backoff_factor: 0.5
    failure_threshold: 3
    failure_window: 300.0

  - name: SUCCESS-jsonplaceholder-filtered      # JSON validation example
    url: https://jsonplaceholder.typicode.com/posts?userId=1&_limit=3
    method: GET
    headers:
      Accept: application/json
    expected_status_codes: [200]
    response_time_threshold: 2.0
    json_path_checks:
      "$[0].userId": 1
      "$[0].id": 1
      "$[1].userId": 1

  - name: SUCCESS-post-request                  # POST request example
    url: https://httpbin.org/post
    method: POST
    headers:
      Content-Type: application/json
      X-API-Key: ${API_KEY:-test-key-123}
    body:
      name: "test"
      check: "health"
    expected_status_codes: [200]
    json_path_checks:
      "$.json.name": "test"
      "$.json.check": "health"
```

### Setting Up Alerts

Configure where and how you get notified:

```yaml
alerting:
  providers:
    slack:                          # Slack configuration
      type: slack
      enabled: false                # Disabled by default
      config:
        webhook_url: ${SLACK_WEBHOOK_URL:-https://hooks.slack.com/services/REPLACE/WITH/YOURS}
        channel: "#notifications"
        username: "Health Monitor"
        icon_emoji: ":warning:"
    
    email:                          # Email configuration
      type: email
      enabled: true
      config:
        smtp_server: ${SMTP_SERVER:-localhost}
        smtp_port: ${SMTP_PORT:-1025}
        username: ${SMTP_USERNAME:-username}
        password: ${SMTP_PASSWORD:-password}
        use_tls: ${SMTP_TLS:-false}
        from_address: "monitor@example.com"
        to_addresses:
          - "admin@example.com"
  
  cooldown_period: 300.0            # Wait between sending same alert (seconds)
  max_alerts_per_hour: 10           # Prevent alert storms
  
  templates:                        # Customise alert messages
    critical: |
      🚨 CRITICAL: Health check failed for {endpoint_name}

      URL: {url}
      Status: {status_code}
      Response Time: {response_time}
      Error: {message}

      Timestamp: {timestamp}

      Please investigate immediately.
```

### General Settings

```yaml
logging:
  level: INFO                      # How verbose (DEBUG, INFO, WARNING, ERROR)
  format: json                     # Log format (json or text)
  output: stdout                   # Where to send logs

concurrency_limit: 10              # Maximum parallel health checks
```

### Using Environment Variables

Keep sensitive data out of your config file:

```yaml
headers:
  Authorization: Basic ${BASIC_AUTH:-dXNlcjpwYXNz}
  X-API-Key: ${API_KEY:-test-key-123}
```

## Command Line Options

```bash
# Basic usage
healthcheck-monitor --config config.yaml

# Override log level
healthcheck-monitor --config config.yaml --log-level DEBUG

# Just check if your config is valid
healthcheck-monitor --config config.yaml --validate-only

# Test mode (doesn't send real alerts)
healthcheck-monitor --config config.yaml --mock-alerts
```

## Docker Examples

```bash
# Mount your config from the host
docker run -v $(pwd)/config:/config ghcr.io/braveokafor/healthchecker-py --config /config/config.yaml

# Pass in environment variables
docker run -e SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXX \
           -v $(pwd)/config:/config \
           ghcr.io/braveokafor/healthchecker-py --config /config/config.yaml
```

## Docker Compose Example

```yaml
services:
  healthchecker:
    image: ghcr.io/braveokafor/healthchecker-py:latest
    volumes:
      - ./examples:/config
    environment:
      - SMTP_USERNAME=user
      - SMTP_PASSWORD=pass
      - SMTP_SERVER="mailhog"
      - SMTP_PORT="1025"
      - SMTP_TLS="false"
    restart: unless-stopped
    command: --config /config/config.yaml
    depends_on:
      - mailhog

  # For testing email alerts locally
  mailhog:
    image: mailhog/mailhog:v1.0.1
    ports:
      - "8025:8025" # Web UI
      - "1025:1025" # SMTP
```

## Response Validation Examples

### JSONPath Checks

```yaml
json_path_checks:
  "$[0].userId": 1                    # Array element property
  "$[0].id": 1                        # Numeric comparison
  "$.json.name": "test"               # Nested property
  "$.json.check": "health"            # String value
  "$.headers.X-Api-Key": "test-key-123" # Check request headers reflected in response
```

### Regex Checks

```yaml
regex_checks:
  title_present: "<h1>Herman Melville - Moby-Dick</h1>"
  paragraph_contains: "It was the Bottle Conjuror"
```

## Project Structure

If you're interested in contributing or understanding the code:

```
healthchecker/
├── __init__.py
├── setup.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── healthchecker/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── models.py        # Configuration data models
│   │   └── loader.py        # Configuration loading & validation
│   ├── monitoring/
│   │   ├── __init__.py
│   │   ├── checker.py       # Main monitoring system
│   │   ├── endpoint.py      # Endpoint checker
│   │   └── response_parser.py # Response validation
│   ├── alerting/
│   │   ├── __init__.py
│   │   ├── manager.py       # Alert management
│   │   ├── providers/
│   │   │   ├── __init__.py
│   │   │   ├── base.py      # Base alert provider
│   │   │   ├── slack.py     # Slack integration
│   │   │   └── email.py     # Email integration
│   ├── utils/
│   │   ├── __init__.py
│   │   └── logging.py       # Logging utilities
│   └── cli.py               # Command line interface
└── tests/                   # Test suite
```

## Extending the System

### Adding a New Alert Provider

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

2. Register your provider:

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

## Testing

```bash
# Run all tests
make test

# Run specific test file
pytest tests/test_config.py
```

## Deployment Tips

### Security Best Practices

Store sensitive info in environment variables:

```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/XXX"
export SMTP_USERNAME="username" 
export SMTP_PASSWORD="password"
export BASIC_AUTH="dXNlcjpwYXNz"  # Base64 of "user:pass"
```

### Resource Usage

Memory and CPU usage scale with the number of endpoints. To optimise:

- Adjust `concurrency_limit` based on your system
- Use longer intervals for non-critical services
- Set appropriate timeouts

## Troubleshooting

### Common Issues

1. **Connection Problems**
   - Check network connectivity
   - Verify firewall settings

2. **Alert Delivery Issues**
   - Confirm provider credentials
   - Check rate limiting settings

3. **Performance Problems**
   - Lower concurrency limit
   - Increase check intervals
   - Optimise validation settings

Enable debug logging for more details:

```bash
healthcheck-monitor --config config.yaml --log-level DEBUG
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file.


[link_issues]:https://github.com/braveokafor/healthchecker-py/issues
[link_pulls]:https://github.com/braveokafor/healthchecker-py/pulls
[link_build_status]:https://github.com/braveokafor/healthchecker-py/actions/workflows/main.yml
[link_build_status]:https://github.com/braveokafor/healthchecker-py/actions/workflows/release.yaml

[badge_issues]:https://img.shields.io/github/issues-raw/braveokafor/healthchecker-py?style=flat-square&logo=GitHub
[badge_pulls]:https://img.shields.io/github/issues-pr/braveokafor/healthchecker-py?style=flat-square&logo=GitHub
[badge_build_status]:https://img.shields.io/github/actions/workflow/status/braveokafor/healthchecker-py/main.yml?style=flat-square&logo=GitHub&label=build
[badge_release_status]:https://img.shields.io/github/actions/workflow/status/braveokafor/healthchecker-py/release.yaml?style=flat-square&logo=GitHub&label=release
