# Health Check Monitor

A production-grade automated health monitoring system for web services built with Python and asyncio.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
[![Build Status][badge_build_status]][link_build_status]
[![Release Status][badge_release_status]][link_build_status]
[![Issues][badge_issues]][link_issues]
[![Pull Requests][badge_pulls]][link_pulls]

## Overview

Health Check Monitor helps you keep an eye on your web services by continuously checking their health status. Built with performance in mind, it can handle monitoring hundreds of endpoints simultaneously while using minimal resources.

## Key Features

- **Fast & Efficient** - Built on asyncio to monitor 1000+ endpoints without breaking a sweat
- **Smart Validation** - Check status codes, response times, JSON content, and regex patterns
- **Alert Management** - Configurable thresholds and cooldown periods to prevent alert fatigue
- **Multiple Notifications** - Send alerts to Slack, Email, or add your own channels
- **Battle-tested Reliability** - Built-in retries, circuit breakers, and self-healing
- **Easy Deployment** - Ready-to-use Docker image and `docker-compose.yaml` for quick setup

## License

This project is licensed under the MIT License - see the LICENSE file for details.


[link_issues]:https://github.com/braveokafor/healthchecker-py/issues
[link_pulls]:https://github.com/braveokafor/healthchecker-py/pulls
[link_build_status]:https://github.com/braveokafor/healthchecker-py/actions/workflows/main.yml
[link_build_status]:https://github.com/braveokafor/healthchecker-py/actions/workflows/release.yaml

[badge_issues]:https://img.shields.io/github/issues-raw/braveokafor/healthchecker-py?style=flat-square&logo=GitHub
[badge_pulls]:https://img.shields.io/github/issues-pr/braveokafor/healthchecker-py?style=flat-square&logo=GitHub
[badge_build_status]:https://img.shields.io/github/actions/workflow/status/braveokafor/healthchecker-py/main.yml?style=flat-square&logo=GitHub&label=build
[badge_release_status]:https://img.shields.io/github/actions/workflow/status/braveokafor/healthchecker-py/release.yaml?style=flat-square&logo=GitHub&label=release
