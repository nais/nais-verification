import logging

from pydantic import BaseSettings
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

from nais_verification.auth import BearerAuth


LOG = logging.getLogger(__name__)


class Settings(BaseSettings):
    CONSOLE_API_URL: str
    CONSOLE_API_TOKEN: str


def create_team():
    settings = Settings()
    auth = BearerAuth(settings.CONSOLE_API_TOKEN)
    transport = RequestsHTTPTransport(settings.CONSOLE_API_URL, auth=auth, verify=True)
    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = gql(  # TODO: Correct query
        """
        mutation CreateTeam {}
        """
    )
    LOG.info(f"Creating team by issuing query:\n{query}")
    result = client.execute(query)
    LOG.info(result)
