import logging
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Optional

from .base import AlertProvider
from ...monitoring.endpoint import CheckResult

logger = logging.getLogger(__name__)


class EmailProvider(AlertProvider):
    """Alert provider for Email."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.smtp_server = config.get("smtp_server", "localhost")
        self.smtp_port = int(config.get("smtp_port", 25))
        self.username = config.get("username")
        self.password = config.get("password")
        self.from_address = config.get("from_address")
        self.to_addresses = config.get("to_addresses", [])

        use_tls_value = config.get("use_tls", False)
        if isinstance(use_tls_value, str):
            self.use_tls = use_tls_value.lower() == "true"
        else:
            self.use_tls = bool(use_tls_value)

        if not self.from_address or not self.to_addresses:
            logger.error("Email from_address and to_addresses are required")
            self.enabled = False

    async def send_alert(
        self, result: CheckResult, template: Optional[str] = None
    ) -> bool:
        """Send an alert via email."""
        if not self.enabled or not self.from_address or not self.to_addresses:
            return False

        try:
            # Format the message
            message_text = self.format_message(result, template)

            # Create the email
            msg = MIMEMultipart("alternative")
            msg["Subject"] = (
                f"Health Check Alert: {result.endpoint_name} - {result.status.value.capitalize()}"
            )
            msg["From"] = self.from_address
            msg["To"] = ", ".join(self.to_addresses)

            # Add text part
            part = MIMEText(message_text, "plain")
            msg.attach(part)

            # Connect to SMTP server
            context = ssl.create_default_context() if self.use_tls else None

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                # Start TLS if required
                if self.use_tls:
                    server.starttls(context=context)

                # Login if credentials provided
                if self.username and self.password:
                    server.login(self.username, self.password)

                # Send the email
                server.send_message(msg)

            logger.info(f"Successfully sent email alert for {result.endpoint_name}")
            return True

        except Exception as e:
            logger.error(f"Error sending email alert: {str(e)}")
            return False
