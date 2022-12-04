#!./bin/python

import logging

from sarayulib.cmd.compile import compile_contracts
from sarayulib.cmd.setup import account_setup
from sarayulib.cmd.deploy import deploy_contract

logging.basicConfig(level=logging.DEBUG, format="%(message)s")

compile_contracts(())
account_setup("STARKNET_PRIVATE_KEY")
deploy_contract("game", alias="game")
