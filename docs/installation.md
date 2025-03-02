# Installation

There are multiple ways to install and run Health Check Monitor, depending on your preferences and requirements.

## Docker Quick Start

The fastest way to try Health Check Monitor:

1. Clone the repository:

```bash
git clone https://github.com/braveokafor/healthchecker-py.git
cd healthchecker-py
```

2. Run with docker-compose:

```bash
docker compose up
```

That's it! The monitoring system is now running with our example configuration.

3. See it in action:
   - Open [http://localhost:8025](http://localhost:8025) in your browser to access the MailHog UI
   - You'll see alert emails arriving as some test endpoints fail
   - The emails show information about why the endpoints are failing

4. Explore what's happening:
   - Check the example configuration at `examples/config.yaml` to see what's being monitored
   - View the docker-compose setup in `docker-compose.yaml` to understand the components
   - Look at container logs to see real-time monitoring output

When you're done exploring, press `Ctrl+C` or run `docker compose down` to stop all services.

## Standard Installation

### Prerequisites

- Python 3.9+
- pip

### From Source

```bash
git clone https://github.com/braveokafor/healthchecker-py.git
cd healthchecker-py
pip install -e .
```

### Using Docker

```bash
docker pull ghcr.io/braveokafor/healthchecker-py:latest
```