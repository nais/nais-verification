#!/usr/bin/env python
import argparse
import enum
import logging

from fiaas_logging import init_logging
from gql.transport.requests import log as requests_logger

from nais_verification.team import create_team  # NOQA: Imported for dynamic lookup
from nais_verification.deploy_key import create_deploy_key  # NOQA: Imported for dynamic lookup


class Actions(enum.Enum):
    @staticmethod
    def _generate_next_value_(name: str, *args) -> str:
        return name.lower().replace("_", "-")

    CREATE_TEAM = enum.auto()
    CREATE_DEPLOY_KEY = enum.auto()

    def __str__(self):
        return self.value

    def execute(self, dry_run):
        func = globals().get(self.name.lower())
        if not func:
            raise RuntimeError(f"No function defined for action {self.value}")
        func(dry_run)


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
