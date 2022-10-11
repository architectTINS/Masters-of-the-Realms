#!./bin/python

import sys
import logging

from starknet_wrapper import wrapped_send
from nile.core.call_or_invoke import call_or_invoke
import game_library as lib

logging.basicConfig(level=logging.DEBUG, format="%(message)s")
#logging.basicConfig(level=logging.INFO, format="%(message)s")

def play_full_game():
    logging.info(f'\n\n-- Enrolling all players... All their initial balances are set to 1000 pearls.\n')
    lib.init_pearls_for_all_players()

    logging.info(f'\n\n-- Initialising target price for all 3 markets (options) ...\n')
    lib.init_food_data_for_all_options()

    logging.info(f'\n\n-- Initialising game state. ...\n')
    lib.reset_game_state()

    for i in range(lib.get_number_of_rounds()):
        round = i + 1

        logging.info(f'\n-- Set food choices for round {round}...\n')
        lib.set_choices_for_the_round(round)

        logging.info(f'\n-- commit the order for round {round} for all players ...\n')
        out = lib.commit_food_order(round)

        if (out == 0):
            print(f'Problem with the order. Order invalidated.')

        lib.get_game_data_after_a_round(round)

if __name__ == "__main__":
    play_full_game()
