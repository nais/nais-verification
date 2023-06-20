import logging
from pprint import pformat

from gql import Client, gql
from gql.transport.exceptions import TransportQueryError
from gql.transport.requests import RequestsHTTPTransport
from k8s import config
from k8s.models.common import ObjectMeta
from k8s.models.secret import Secret

from nais_verification.auth import BearerAuth
from nais_verification.settings import Settings

LOG = logging.getLogger(__name__)


def create_deploy_key(dry_run: bool):
    settings = Settings()
    deploy_key = _get_team_deploy_key(settings)
    _save_key_to_cluster(dry_run, settings, deploy_key)


def _configure_k8s(settings: Settings):
    if not settings.K8S_API_URL:
        LOG.info("Using in-cluster config for k8s")
        config.use_in_cluster_config()
        return
    config.api_server = settings.K8S_API_URL
    config.api_token = settings.K8S_API_TOKEN
    if settings.K8S_API_CA_PATH:
        config.verify_ssl = settings.K8S_API_CA_PATH
    if settings.K8S_API_CERT_PATH and settings.K8S_API_KEY_PATH:
        config.cert = (settings.K8S_API_CERT_PATH, settings.K8S_API_KEY_PATH)
    LOG.info("Using supplied config for k8s server at %s", settings.K8S_API_URL)


def _save_key_to_cluster(dry_run: bool, settings: Settings, deploy_key: str):
    _configure_k8s(settings)
    object_meta = ObjectMeta(name=settings.SECRET_NAME, namespace=settings.SECRET_NAMESPACE)
    secret = Secret.get_or_create(metadata=object_meta)
    secret.stringData = {"DEPLOY_API_KEY": deploy_key}
    if dry_run:
        LOG.info("Would have saved secret to cluster:\n %s", pformat(secret.as_dict()))
    else:
        secret.save()
        LOG.info("Created secret %s", object_meta)


def _get_team_deploy_key(settings: Settings) -> str:
    auth = BearerAuth(settings.NAIS_TEAMS_API_TOKEN)
    transport = RequestsHTTPTransport(settings.NAIS_TEAMS_API_URL, auth=auth, verify=True)
    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = gql(
        """
        query getDeployKey($slug: Slug!) {
          deployKey(slug: $slug)
        }
        """
    )
    params = {
        "slug": settings.TEAM_NAME,
    }
    LOG.info("Get team deploy key for team %r", settings.TEAM_NAME)
    try:
        result = client.execute(query, variable_values=params)
        LOG.debug("result from getDeployKey query: %s", pformat(result))
        deploy_key = result.get("deployKey", "")
        return deploy_key
    except TransportQueryError as e:
        LOG.error("Failed to get deploy key:\n\t%s", _format_errors(e))
        raise RuntimeError("Failed to get deploy key") from e


def _format_errors(e):
    return "\n\t".join(err["message"] for err in e.errors)
