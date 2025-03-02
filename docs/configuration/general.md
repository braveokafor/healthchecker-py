# General Settings

Configure global settings for your monitoring system.

## Logging Configuration

Control how logs are generated and where they're sent:

```yaml
logging:
  level: INFO                      # How verbose (DEBUG, INFO, WARNING, ERROR)
  format: json                     # Log format (json or text)
  output: stdout                   # Where to send logs
```

## Concurrency Settings

Control resource usage by limiting parallel operations:

```yaml
concurrency_limit: 10              # Maximum parallel health checks
```

## Using Environment Variables

Keep sensitive data out of your configuration file by using environment variables:

```yaml
headers:
  Authorization: Basic ${BASIC_AUTH:-dXNlcjpwYXNz}
  X-API-Key: ${API_KEY:-test-key-123}
```

The format `${ENV_VAR:-default}` means:
- Use the value of `ENV_VAR` if it exists
- Otherwise, use the value after `:-` as default

### Setting Environment Variables

```bash
# Set variables before running
export API_KEY="your-secret-key"
export BASIC_AUTH="base64-encoded-credentials"

# Then run with these variables available
healthchecker --config config.yaml
```

For Docker, you can pass environment variables using the `-e` flag:

```bash
docker run -e API_KEY="your-secret-key" \
           -v $(pwd)/config:/config \
           ghcr.io/braveokafor/healthchecker-py --config /config/config.yaml
```