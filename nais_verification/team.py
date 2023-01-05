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

    if not _team_exists(client, settings):
        _create_team(client, dry_run, settings)


def _team_exists(client, settings):
    query = gql(
        """
        query team($slug: Slug!) {
          team(slug: $slug) {
            slug
            syncErrors {
              error
            }
          }
        }
        """
    )
    params = {
        "slug": settings.TEAM_NAME,
    }
    LOG.info("Looking up team %r", settings.TEAM_NAME)
    result = client.execute(query, variable_values=params)
    LOG.info(result)
    data = result.get("data", {})
    team = data.get("team", {})
    return team.get("slug") == settings.TEAM_NAME


def _create_team(client, dry_run, settings):
    mutation = gql(
        """
        mutation createTeam($slug: Slug!, $purpose: String!, $slackAlertsChannel: String!) {
          createTeam(input: {
            slug: $slug,
            purpose: $purpose,
            slackAlertsChannel: $slackAlertsChannel
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
        "slackAlertsChannel": settings.TEAM_CHANNEL,
    }
    LOG.info("Creating team %r", settings.TEAM_NAME)
    if not dry_run:
        result = client.execute(mutation, variable_values=params)
        LOG.info(result)
