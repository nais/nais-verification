from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl


class Settings(BaseSettings):
    NAIS_TEAMS_API_URL: AnyHttpUrl
    NAIS_TEAMS_API_TOKEN: str

    # Only need to override these when running outside a cluster
    K8S_API_URL: Optional[AnyHttpUrl] = None
    K8S_API_TOKEN: Optional[str] = ""
    K8S_API_CERT_PATH: Optional[Path] = None
    K8S_API_KEY_PATH: Optional[Path] = None
    K8S_API_CA_PATH: Optional[Path] = None

    TEAM_NAME: str = "nais-verification"
    TEAM_PURPOSE: str = "A place for NAIS to run verification workloads"
    TEAM_CHANNEL: str = "#nais"

    SECRET_NAME: str = "nais-verification-deploy-key"
    SECRET_NAMESPACE: str = "nais-system"

    LOG_LEVEL: str = "INFO"
