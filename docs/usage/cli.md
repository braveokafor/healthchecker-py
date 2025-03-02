# Command Line Options

Health Check Monitor provides several command line options to control its behavior.

## Available Options

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

## Option Details

| Option | Description |
|--------|-------------|
| `--config` | Path to configuration file (required) |
| `--log-level` | Override logging level (DEBUG, INFO, WARNING, ERROR) |
| `--validate-only` | Validate configuration without starting monitoring |
| `--mock-alerts` | Run with mock alerts (alerts are logged but not sent) |
| `--help` | Show help message and exit |

## Environment Variables

In addition to command line options, you can use environment variables to control behavior or provide sensitive information. See [General Settings](../configuration/general.md) for more details.