import logging

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

from nais_verification.auth import BearerAuth
from nais_verification.settings import Settings

LOG = logging.getLogger(__name__)


def create_team(dry_run: bool):
    settings = Settings()
    auth = BearerAuth(settings.CONSOLE_API_TOKEN)
    transport = RequestsHTTPTransport(settings.CONSOLE_API_URL, auth=auth, verify=True)
    client = Client(transport=transport, fetch_schema_from_transport=True)

    mutation = gql(
        """
        mutation createTeam($slug: Slug!, $purpose: String!) {
          createTeam(input: {
            slug: $slug,
            purpose: $purpose
          }) {
            syncErrors {
              reconciler,
              error
            }
          }
        }
        """
    )
    params = {
        "slug": settings.TEAM_NAME,
        "purpose": settings.TEAM_PURPOSE,
    }
    LOG.info("Creating team %r", settings.TEAM_NAME)
    if not dry_run:
        result = client.execute(mutation, variable_values=params)
        LOG.info(result)
