#!./bin/python

import sys
import logging

import game_library as lib

logging.basicConfig(level=logging.DEBUG, format="%(message)s")
#logging.basicConfig(level=logging.INFO, format="%(message)s")

def test_players_pearls_init():
    logging.info(f'\n\n-- Test: Initialising all players...\n')

    lib.init_pearls_for_all_players()

    round_num = 0
    for player_id in [8,9,3]:
        out = lib.get_pearls_balance(player_id, round_num)
        logging.info(f'Initial pearls balance for player {player_id}: {out}')

    for player_id in [0,11]:
        out = lib.get_pearls_balance(player_id, round_num)
        logging.info(f'Initial pearls balance for non-existing player {player_id}: {out}')

    player_id = 1; round_num = 1
    out = lib.get_pearls_balance(player_id, round_num)
    logging.info(f'Pearls balance for player {player_id} in any other round(Round {round_num} here): {out}')

    logging.info(f'=====  TEST COMPLETE =====')
    input("Press Enter to continue...")

def test_food_price_init():
    logging.info(f'\n\n-- Test: Initialising food data for all options...\n')

    lib.init_food_data_for_all_options()

    round_num = 0
    for option_id in [1,3]:
        out = lib.get_food_price(option_id, round_num)
        logging.info(f'Initial Target price for food option {option_id}: {out}')

    for option_id in [0,4]:
        out = lib.get_food_price(option_id, round_num)
        logging.info(f'Initial Target price for non-existing food option {option_id}: {out}')

    out = lib.get_food_price(option_id=1, round_num=1)
    logging.info(f'Initial Target price for any other round (round 1 here ) for food option 4: {out}')

    logging.info(f'=====  TEST COMPLETE =====')
    input("Press Enter to continue...")

def test_set_choices_for_the_round():
    logging.info(f'\n\n-- Test: Set Food choices for the round...\n')

    for round in [1,5]:
        logging.info(f'\n-- Set food choices for round {round}...\n')
        lib.set_choices_for_the_round(round)
        out = lib.get_food_options_demand_for_all_options()
        print(f'Round {round}: Demand for each food option: {out}')
        input("Press Enter to continue...")

    for invalid_round_number in [0,11]:
        ## Throws an assertion in python code.
        logging.info(f'\n-- Set food choices for invalid round number {invalid_round_number}...\n')
        lib.set_choices_for_the_round(invalid_round_number)
        input("Press Enter to continue...")

    logging.info(f'=====  TEST COMPLETE =====')
    input("Press Enter to continue...")

def test_resetting_food_options_demand():
    logging.info(f'\n\n-- Test: Set and reset food choices ...\n')
    round = 1
    lib.set_choices_for_the_round(round)
    out = lib.get_food_options_demand_for_all_options()
    logging.info(f'Number of players opting for each food option in Round {round} : {out}')
    input("Press Enter to continue...")

    print(f'\n --- Resetting the demand for food options --- \n')
    lib.reset_food_options_demand()
    out = lib.get_food_options_demand_for_all_options()
    print(f'Food choices after reset: {out}')

    logging.info(f'=====  TEST COMPLETE =====')
    input("Press Enter to continue...")

# Make sure to call init_food_data_for_all_options()
# before this function. Also, food choices must be set.
def test_calculate_food_price():
    logging.info(f'\n\n-- Test: Set food choices and calculate prices ...\n')

    round = 1
    lib.set_choices_for_the_round(round)
    out = lib.get_food_options_demand_for_all_options()
    print(f'Round {round}: Demand for each food option: {out}')
    out = lib.calculate_food_price(round)
    print(f'Round {round}: Price for each food option in Uint256 format: {out[0]}')

    logging.info(f'=====  TEST COMPLETE =====')
    input("Press Enter to continue...")

# Choices must be set before commit food order.
def test_commit_food_order(round):
    logging.info(f'\n\n-- Test: commit the order for round {round} for all players ...\n')

    logging.info(f'\n-- Set food choices for day {round}...\n')
    lib.set_choices_for_the_round(round)

    out = lib.commit_food_order(round)

    if (out == 0):
        print(f'Problem with the order. Order invalidated.')

def test_check_game_data_after_food_order(round):
    lib.get_game_data_after_a_round(round)


if __name__ == "__main__":
    #test_players_pearls_init()
    #test_food_price_init()

    #test_set_choices_for_the_round()
    #test_resetting_food_options_demand()
    #test_calculate_food_price()

    #test_commit_food_order(1)
    #test_check_game_data_after_food_order(2)

    #test_commit_food_order(7)
    #test_commit_food_order(8)
    #test_commit_food_order(9)
    #test_commit_food_order(10)
    #test_check_variables_after_food_order(7)
    #test_check_variables_after_food_order(8)
    #test_check_variables_after_food_order(9)
    #test_check_variables_after_food_order(10)

    print("")

# ToDo:
# Asserts
