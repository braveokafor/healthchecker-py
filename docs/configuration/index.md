# Configuration

Your configuration file is the heart of the system. This section covers everything you need to know about configuring Health Check Monitor.

## Quick Start

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
healthchecker --config config.yaml --mock-alerts
```

## Configuration Structure

The configuration file is organized into several main sections:

- **[Endpoints](endpoints.md)** - Define what services to monitor
- **[Alerting](alerting.md)** - Configure alerts and notifications
- **[General Settings](general.md)** - Set up logging and performance parameters

Each section has its own configuration options and examples, which are covered in detail on their respective pages.