# Project Structure

If you're interested in contributing or understanding the code, here's an overview of the project structure:

```
healthchecker/
├── __init__.py
├── setup.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── healthchecker/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── models.py        # Configuration data models
│   │   └── loader.py        # Configuration loading & validation
│   ├── monitoring/
│   │   ├── __init__.py
│   │   ├── checker.py       # Main monitoring system
│   │   ├── endpoint.py      # Endpoint checker
│   │   └── response_parser.py # Response validation
│   ├── alerting/
│   │   ├── __init__.py
│   │   ├── manager.py       # Alert management
│   │   ├── providers/
│   │   │   ├── __init__.py
│   │   │   ├── base.py      # Base alert provider
│   │   │   ├── slack.py     # Slack integration
│   │   │   └── email.py     # Email integration
│   ├── utils/
│   │   ├── __init__.py
│   │   └── logging.py       # Logging utilities
│   └── cli.py               # Command line interface
└── tests/                   # Test suite
```

## Key Components

The system is organized into several key components:

- **Configuration** - Handles loading and validating configuration files
- **Monitoring** - Manages health checks and response validation
- **Alerting** - Sends notifications when checks fail
- **Utils** - Provides common utilities and helpers
- **CLI** - Implements the command line interface

This modular structure makes it easy to understand, maintain, and extend the system.