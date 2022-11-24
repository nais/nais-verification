#!/usr/bin/env python
import argparse
import enum
import logging

from fiaas_logging import init_logging
from gql.transport.requests import log as requests_logger

from nais_verification.team import create_team  # NOQA: Imported for dynamic lookup
from nais_verification.deploy_key import create_deploy_key  # NOQA: Imported for dynamic lookup


class Actions(enum.Enum):
    def __new__(cls, func):
        obj = object.__new__(cls)
        obj.execute = func
        obj._value_ = func.__name__.replace("_", "-")
        return obj

    def __str__(self):
        return self.value

    CREATE_TEAM = (create_team,)
    CREATE_DEPLOY_KEY = (create_deploy_key,)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", help="Which action to take", choices=Actions, type=Actions)
    parser.add_argument("-n", "--dry-run", help="Do a dry run, with no actual action taken", action="store_true")
    init_logging()
    requests_logger.setLevel(logging.WARNING)
    options = parser.parse_args()
    options.action.execute(options.dry_run)


if __name__ == '__main__':
    main()
