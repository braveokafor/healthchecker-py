# Contributing

Contributions to Health Check Monitor are welcome! This guide explains how to contribute effectively.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up the development environment:

```bash
git clone https://github.com/yourusername/healthchecker-py.git
cd healthchecker-py
make virtualenv
```

## Development Workflow

1. Create a branch for your changes:

```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and add tests
3. Ensure all tests pass:

```bash
make test
```

4. Update documentation if needed
5. Commit your changes with a clear message
6. Push your branch and create a pull request

## Coding Standards

- Follow PEP 8 style guidelines
- Include docstrings for all functions, classes, and modules
- Write comprehensive tests for new functionality
- Maintain backward compatibility when possible

## Testing

All new functionality should include tests:

```bash
# Run specific tests
pytest tests/test_file.py
```

## Documentation

Update documentation for any changes:

- Add docstrings to code
- Update relevant parts of the documentation
- Create examples for new features

## Pull Request Process

1. Update the README.md or documentation with details of changes
2. Update the version number in appropriate files
3. The PR will be merged once it has been reviewed and approved

## Code of Conduct

- Be respectful and inclusive
- Focus on the technical merits of contributions
- Help others and provide constructive feedback
- Respect the time and effort of maintainers

Thank you for contributing to Health Check Monitor!