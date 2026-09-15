from pathlib import Path

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    NAIS_TEAMS_API_URL: AnyHttpUrl
    NAIS_TEAMS_API_TOKEN: str

    # Only need to override these when running outside a cluster
    K8S_API_URL: AnyHttpUrl | None = None
    K8S_API_TOKEN: str | None = ""
    K8S_API_CERT_PATH: Path | None = None
    K8S_API_KEY_PATH: Path | None = None
    K8S_API_CA_PATH: Path | None = None

    TEAM_NAME: str = "nais-verification"
    TEAM_PURPOSE: str = "A place for NAIS to run verification workloads"
    TEAM_CHANNEL: str = "#nais"

    SECRET_NAME: str = "nais-verification-deploy-key"
    SECRET_NAMESPACE: str = "nais-system"

    LOG_LEVEL: str = "INFO"
