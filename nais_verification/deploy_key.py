import logging
from pprint import pformat

from gql import Client, gql
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
    LOG.info("Using supplied config for k8s server at {}", settings.K8S_API_URL)


def _save_key_to_cluster(dry_run: bool, settings: Settings, deploy_key: str):
    _configure_k8s(settings)
    object_meta = ObjectMeta(name=settings.SECRET_NAME, namespace=settings.TEAM_NAME)
    secret = Secret.get_or_create(metadata=object_meta)
    secret.stringData["DEPLOY_API_KEY"] = deploy_key
    if dry_run:
        LOG.info("Would have saved secret to cluster:\n {}", pformat(secret.as_dict()))
    else:
        secret.save()
        LOG.info("Created secret {}", object_meta)


def _get_team_deploy_key(settings: Settings) -> str:
    auth = BearerAuth(settings.CONSOLE_API_TOKEN)
    transport = RequestsHTTPTransport(settings.CONSOLE_API_URL, auth=auth, verify=True)
    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = gql(  # TODO: Correct query
        """
        query GetTeam {}
        """
    )
    LOG.info(f"Get team deploy key using query:\n{query}")
    result = client.execute(query)
    LOG.info(result)
    return result
