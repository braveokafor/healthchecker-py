# Setting Up Alerts

Configure how and where you'll be notified when endpoints have issues.

## Alert Providers

Health Check Monitor supports multiple alert providers that can be enabled simultaneously.

### Slack Configuration

```yaml
alerting:
  providers:
    slack:
      type: slack
      enabled: false
      config:
        webhook_url: ${SLACK_WEBHOOK_URL:-https://hooks.slack.com/services/REPLACE/WITH/YOURS}
        channel: "#notifications"
        username: "Health Monitor"
        icon_emoji: ":warning:"
```

### Email Configuration

```yaml
alerting:
  providers:
    email:
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
```

## Alert Control Settings

Prevent alert fatigue with these settings:

```yaml
alerting:
  cooldown_period: 300.0            # Wait between sending same alert (seconds)
  max_alerts_per_hour: 10           # Prevent alert storms
```

## Custom Alert Templates

Customize your alert messages with templates:

```yaml
alerting:
  templates:
    critical: |
      🚨 CRITICAL: Health check failed for {endpoint_name}

      URL: {url}
      Status: {status_code}
      Response Time: {response_time}
      Error: {message}

      Timestamp: {timestamp}

      Please investigate immediately.
```

## Using Environment Variables

For security, store sensitive alert provider credentials as environment variables:

```yaml
alerting:
  providers:
    slack:
      config:
        webhook_url: ${SLACK_WEBHOOK_URL:-default_fallback_value}
```

For more information on using environment variables, see [General Settings](general.md).