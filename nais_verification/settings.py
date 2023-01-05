from pathlib import Path

from pydantic import BaseSettings, HttpUrl


class Settings(BaseSettings):
    CONSOLE_API_URL: HttpUrl
    CONSOLE_API_TOKEN: str

    # Only need to override these when running outside a cluster
    K8S_API_URL: HttpUrl = None
    K8S_API_TOKEN: str = ""
    K8S_API_CERT_PATH: Path = ""
    K8S_API_KEY_PATH: Path = ""
    K8S_API_CA_PATH: Path = ""

    TEAM_NAME: str = "nais-verification"
    TEAM_PURPOSE: str = "A place for NAIS to run verification workloads"
    TEAM_CHANNEL: str = "#nais"

    SECRET_NAME: str = "nais-verification-deploy-key"
    SECRET_NAMESPACE: str = "nais-system"

    LOG_LEVEL: str = "WARNING"
