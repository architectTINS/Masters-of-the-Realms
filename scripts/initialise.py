#!./bin/python

import logging
from nile.core.account import Account
from nile.core.deploy import deploy

logging.basicConfig(level=logging.DEBUG, format="%(message)s")

Account("STARKNET_PRIVATE_KEY", "localhost")

deploy("balance", None, alias="balance", network="localhost")
