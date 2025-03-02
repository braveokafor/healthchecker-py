# Troubleshooting

This guide helps you diagnose and fix common issues with Health Check Monitor.

## Common Issues

### Connection Problems

If you're seeing connection errors:

- Check network connectivity
- Verify firewall settings
- Ensure DNS resolution is working
- Check for TLS/SSL configuration issues
- Confirm proxy settings if applicable

### Alert Delivery Issues

If alerts aren't being delivered:

- Confirm provider credentials are correct
- Check rate limiting settings
- Verify network connectivity to alert services
- Ensure notification service is operational
- Check spam filters for email alerts

### Performance Problems

If the system is using excessive resources:

- Lower the `concurrency_limit` setting
- Increase check intervals for non-critical services
- Set appropriate timeouts
- Optimize validation settings
- Check for memory leaks or resource-intensive endpoints

## Debugging

Enable debug logging for more detailed information:

```bash
healthcheck-monitor --config config.yaml --log-level DEBUG
```

This will show detailed information about:

- Configuration loading
- Endpoint checking
- Response validation
- Alert delivery

## Log Analysis

Common error patterns to look for:

- Repeated connection timeouts to a specific endpoint
- Consistent validation failures
- Alert delivery failures
- Resource exhaustion warnings

## Getting Help

If you encounter issues that you can't resolve:

1. Check the GitHub issues for similar problems
2. Gather logs and configuration (with sensitive information removed)
3. Open a detailed issue on the GitHub repository