# Basic Usage

This section covers the fundamental usage patterns for Health Check Monitor.

## Starting the Monitor

Once you have a configuration file ready, you can start monitoring:

```bash
healthchecker --config config.yaml
```

## Testing Your Configuration

To validate your configuration without actually sending alerts:

```bash
healthchecker --config config.yaml --mock-alerts
```

## Checking Configuration Validity

To just check if your configuration file is valid:

```bash
healthchecker --config config.yaml --validate-only
```

## Monitoring Process

Once started, Health Check Monitor will:

1. Load your configuration
2. Begin checking endpoints at their specified intervals
3. Validate responses according to your criteria
4. Send alerts when problems are detected
5. Continue monitoring indefinitely (or until stopped)

For more detailed options, see [Command Line Options](cli.md) and [Docker Usage](docker.md).