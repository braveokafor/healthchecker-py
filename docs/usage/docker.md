# Docker Usage

Health Check Monitor provides Docker support for easy deployment.

## Basic Docker Usage

```bash
# Mount your config from the host
docker run -v $(pwd)/config:/config ghcr.io/braveokafor/healthchecker-py --config /config/config.yaml

# Pass in environment variables
docker run -e SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXX \
           -v $(pwd)/config:/config \
           ghcr.io/braveokafor/healthchecker-py --config /config/config.yaml
```

## Docker Compose Example

Create a `docker-compose.yaml` file:

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

Then start the services:

```bash
docker compose up
```

## Testing With MailHog

The Docker Compose example includes MailHog, a testing tool for email delivery:

1. Start the services with `docker compose up`
2. Open [http://localhost:8025](http://localhost:8025) in your browser
3. Any email alerts will be captured and displayed in the MailHog UI

This is a great way to test your configuration without sending real emails.