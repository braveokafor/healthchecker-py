import re
import logging
from typing import Dict, Any
import jsonpath_ng.ext as jsonpath

logger = logging.getLogger(__name__)


def validate_json_paths(
    data: Dict[str, Any], checks: Dict[str, Any]
) -> Dict[str, bool]:
    """
    Validate a JSON response against JSONPath checks.

    Args:
        data: The JSON data to validate
        checks: Dictionary mapping JSONPath expressions to expected values

    Returns:
        Dictionary mapping check names to boolean results
    """
    results = {}

    for path_expr, expected_value in checks.items():
        try:
            # Parse the JSONPath expression
            jsonpath_expr = jsonpath.parse(path_expr)

            # Find all matches
            matches = [match.value for match in jsonpath_expr.find(data)]

            # Check if we found any matches
            if not matches:
                results[path_expr] = False
                continue

            # For simplicity, we consider the first match if multiple exist
            actual_value = matches[0]

            # Compare to expected value
            results[path_expr] = actual_value == expected_value

        except Exception as e:
            logger.error(f"Error evaluating JSONPath {path_expr}: {str(e)}")
            results[path_expr] = False

    return results


def validate_regex_patterns(text: str, patterns: Dict[str, str]) -> Dict[str, bool]:
    """
    Validate text against regex patterns.

    Args:
        text: The text to validate
        patterns: Dictionary mapping pattern names to regex patterns

    Returns:
        Dictionary mapping pattern names to boolean results
    """
    results = {}

    for pattern_name, pattern_str in patterns.items():
        try:
            # Compile the regex pattern
            pattern = re.compile(pattern_str, re.DOTALL)

            # Check if the pattern matches
            match = pattern.search(text)
            results[pattern_name] = match is not None

        except Exception as e:
            logger.error(f"Error evaluating regex pattern {pattern_name}: {str(e)}")
            results[pattern_name] = False

    return results
