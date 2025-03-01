from typing import Dict, List, Optional, Union, Any, Literal
from pydantic import BaseModel, Field, field_validator, model_validator
import re


class RetryConfig(BaseModel):
    attempts: int = Field(default=3, ge=1)
    backoff_factor: float = Field(default=0.3, ge=0)


class EndpointConfig(BaseModel):
    url: str
    name: Optional[str] = None
    method: str = "GET"
    headers: Dict[str, str] = Field(default_factory=dict)
    body: Optional[Union[Dict[str, Any], str]] = None
    expected_status_codes: List[int] = Field(default=[200])
    expected_status_ranges: List[str] = Field(default_factory=list)
    response_time_threshold: float = 5.0  # seconds
    timeout: float = 10.0  # seconds
    interval: float = 60.0  # seconds
    retry: RetryConfig = Field(default_factory=RetryConfig)
    json_path_checks: Dict[str, Any] = Field(default_factory=dict)
    regex_checks: Dict[str, str] = Field(default_factory=dict)
    failure_threshold: int = 3  # failures
    failure_window: float = 300.0  # seconds (5 minutes)

    @model_validator(mode="after")
    def set_default_name(self) -> "EndpointConfig":
        if not self.name and self.url:
            try:
                self.name = self.url.split("://")[-1].split("/")[0]
            except (IndexError, AttributeError):
                self.name = self.url  # Fallback to full URL
        return self

    @field_validator("expected_status_ranges", mode="after")
    @classmethod
    def validate_status_ranges(cls, v):
        for item in v:
            if not re.match(r"^\d{3}-\d{3}$", item):
                raise ValueError(
                    f"Status range must be in format '100-199', got {item}"
                )
            start, end = map(int, item.split("-"))
            if not (100 <= start <= 599 and 100 <= end <= 599 and start <= end):
                raise ValueError(f"Invalid status range: {item}")
        return v


class AlertProviderConfig(BaseModel):
    type: str
    enabled: bool = True
    config: Dict[str, Any] = Field(default_factory=dict)


class AlertConfig(BaseModel):
    providers: Dict[str, AlertProviderConfig]
    cooldown_period: float = 600.0  # seconds
    max_alerts_per_hour: int = 10
    templates: Dict[str, str] = Field(default_factory=dict)


class LoggingConfig(BaseModel):
    level: str = "INFO"
    format: Literal["json", "text"] = "json"
    output: str = "stdout"


class AppConfig(BaseModel):
    endpoints: List[EndpointConfig]
    alerting: AlertConfig
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    concurrency_limit: int = Field(default=100, ge=1)

    @field_validator("endpoints")
    @classmethod
    def validate_unique_names(cls, v):
        names = [endpoint.name for endpoint in v]
        if len(names) != len(set(names)):
            raise ValueError("Endpoint names must be unique")
        return v
