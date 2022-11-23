from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    CONSOLE_API_URL: str
    CONSOLE_API_TOKEN: str

    K8S_API_URL: str = ""
    K8S_API_TOKEN: str = ""
    K8S_API_CERT_PATH: Path = ""
    K8S_API_KEY_PATH: Path = ""
    K8S_API_CA_PATH: Path = ""

    TEAM_NAME: str = "nais-verification"
    SECRET_NAME: str = "deploy-key"
