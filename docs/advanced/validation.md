# Response Validation

Health Check Monitor provides powerful options for validating responses beyond just checking status codes.

## JSONPath Checks

Validate JSON response content using JSONPath expressions:

```yaml
json_path_checks:
  "$[0].userId": 1                    # Array element property
  "$[0].id": 1                        # Numeric comparison
  "$.json.name": "test"               # Nested property
  "$.json.check": "health"            # String value
  "$.headers.X-Api-Key": "test-key-123" # Check request headers reflected in response
```

JSONPath is a query language for JSON, similar to XPath for XML. It allows you to extract and verify specific parts of a JSON response.

## Regex Checks

Validate response body content using regular expressions:

```yaml
regex_checks:
  title_present: "<h1>Herman Melville - Moby-Dick</h1>"
  paragraph_contains: "It was the Bottle Conjuror"
```

Each key is a descriptive name for the check, and the value is the regex pattern to match. If the pattern is not found in the response body, the check fails.

## Combining Validation Methods

You can combine different validation methods in a single endpoint configuration:

```yaml
- name: comprehensive-check
  url: https://api.example.com/status
  method: GET
  expected_status_codes: [200]
  response_time_threshold: 1.0
  json_path_checks:
    "$.status": "healthy"
    "$.version": "1.2.3"
  regex_checks:
    contains_timestamp: "\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}"
```

This provides flexible and powerful validation options for any type of endpoint.