# Monitoring Endpoints

This section explains how to configure the endpoints you want to monitor.

## Basic Configuration

Each endpoint is defined as an item in the `endpoints` array with the following properties:

- `name`: A unique identifier for the endpoint
- `url`: The URL to monitor
- `method`: HTTP method to use (GET, POST, etc.)
- `expected_status_codes`: List of status codes considered healthy
- `response_time_threshold`: Maximum acceptable response time in seconds
- `interval`: How often to check the endpoint (in seconds)

## Examples

### Simple Status Check

```yaml
- name: SUCCESS-httpbin-status
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
```

### JSON Validation Example

```yaml
- name: SUCCESS-jsonplaceholder-filtered
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
```

### POST Request Example

```yaml
- name: SUCCESS-post-request
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

## Advanced Configuration

For more advanced validation options, see the [Response Validation](../advanced/validation.md) section.