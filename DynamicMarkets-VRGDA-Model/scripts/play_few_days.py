#!./bin/python

import sys
import logging

from starknet_wrapper import wrapped_send
from nile.core.call_or_invoke import call_or_invoke
import game_library as lib

logging.basicConfig(level=logging.DEBUG, format="%(message)s")
#logging.basicConfig(level=logging.INFO, format="%(message)s")

def play_few_rounds():
    logging.info(f'\n\n-- Enrolling all players... All their initial balances are set to 1000 pearls.\n')
    lib.init_pearls_for_all_players()
    input("Press Enter to continue...")

    logging.info(f'\n\n-- Initialising target price for all 3 markets (options) ...\n')
    lib.init_food_data_for_all_options()
    input("Press Enter to continue...")

    logging.info(f'\n\n-- Initialising game state. ...\n')
    lib.reset_game_state()
    input("Press Enter to continue...")

    round_to_play = 3
    for i in range(round_to_play):
        round = i + 1

        logging.info(f'\n-- Set food choices for day {round}...\n')
        lib.set_choices_for_the_round(round)
        input("Press Enter to continue...")

        logging.info(f'\n-- commit the order for day {round} for all players ...\n')
        out = lib.commit_food_order(round)

        if (out == 0):
            print(f'Problem with the order. Order invalidated.')

        lib.get_game_data_after_a_round(round)
        input("Press Enter to continue...")

if __name__ == "__main__":
    play_few_rounds()