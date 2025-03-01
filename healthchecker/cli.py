import asyncio
import argparse
import logging
import sys
import time

from .config.loader import load_config
from .utils.logging import configure_logging

logger = logging.getLogger(__name__)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Health check monitoring system")

    parser.add_argument(
        "-c",
        "--config",
        help="Path to the YAML configuration file",
        default="config.yaml",
    )

    parser.add_argument(
        "--validate-only",
        help="Only validate the configuration, don't run the monitoring",
        action="store_true",
    )

    parser.add_argument(
        "--log-level",
        help="Set the log level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
    )

    return parser.parse_args()


async def main_async():
    """Main async entry point."""
    args = parse_args()

    try:
        # Load configuration
        config = load_config(args.config)

        # Configure logging
        log_config = config.logging.model_dump()
        if args.log_level:
            log_config["level"] = args.log_level
        configure_logging(log_config)

        logger.info("Starting...")

        # If validate-only, exit successfully
        if args.validate_only:
            logger.info("Configuration validated successfully")
            return 0

        # return 0
        logger.info("Sleeping for 30 seconds")
        time.sleep(30)

    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        return 0
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return 1


def main():
    """Entry point for the CLI."""
    exit_code = asyncio.run(main_async())
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
