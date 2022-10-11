#!./bin/python

import sys
import logging

from starknet_wrapper import wrapped_send
from nile.core.call_or_invoke import call_or_invoke
import game_library as lib

logging.basicConfig(level=logging.DEBUG, format="%(message)s")
#logging.basicConfig(level=logging.INFO, format="%(message)s")


lib.get_game_data_after_a_round(10)
lib.get_demand_vs_pricing_data_for_all_rounds()
lib.get_player_data_for_all_round()
lib.declare_winner()
