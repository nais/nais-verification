import logging
from pprint import pformat

from gql import Client, gql
from gql.transport.exceptions import TransportQueryError
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
    else:
        _sync_team(client, dry_run, settings)


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
    try:
        result = client.execute(query, variable_values=params)
        LOG.debug("result from team query: %s", pformat(result))
        team = result.get("team", {})
        return team.get("slug") == settings.TEAM_NAME
    except TransportQueryError as e:
        LOG.warning("Failed to lookup team:\n\t%s", _format_errors(e))
    return False


def _sync_team(client, dry_run, settings):
    mutation = gql(
        """
        mutation synchronizeTeam($slug: Slug!) {
          synchronizeTeam(slug: $slug) {
            correlationID
          }
        }
        """
    )
    params = {
        "slug": settings.TEAM_NAME,
    }
    LOG.info("Synchronizing team %r", settings.TEAM_NAME)
    if not dry_run:
        try:
            result = client.execute(mutation, variable_values=params)
            LOG.debug("result from synchronizeTeam: %s", pformat(result))
        except TransportQueryError as e:
            LOG.error("Failed to synchronize team:\n\t%s", _format_errors(e))
            raise RuntimeError("Failed to synchronize team") from e


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
        try:
            result = client.execute(mutation, variable_values=params)
            LOG.debug("result from createTeam: %s", pformat(result))
        except TransportQueryError as e:
            LOG.error("Failed to create team:\n\t%s", _format_errors(e))
            raise RuntimeError("Failed to create team") from e


def _format_errors(e):
    return "\n\t".join(err["message"] for err in e.errors)
