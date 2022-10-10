#!./bin/python

import game_library
import constants

from nile.core.call_or_invoke import call_or_invoke
from starknet_wrapper import wrapped_send
from constants import NETWORK
from game_data import MarketID, Choices

def get_number_of_players():
    """
    Get number of players.
    """
    num_players = call_or_invoke("game", "call", "get_number_of_players", None, NETWORK)
    # logging.info(f'Number of players: {num_players}')
    return int(num_players)

def get_number_of_food_options():
    """
    Get number of markets.
    """
    num = call_or_invoke("game", "call", "get_number_of_food_options", None, NETWORK)
    # logging.info(f'Number of markets: {num}')
    return int(num)

## Globals used by the functions.
num_players = get_number_of_players()
num_food_options = get_number_of_food_options()

def init_pearls_for_all_players():
    wrapped_send(NETWORK, "STARKNET_PRIVATE_KEY", "game", "init_pearls_for_all_players", [num_players])
    #out = call_or_invoke("game", "call", "get_pearls_balance", [8,0], NETWORK)
    #print(f"get 3: {out}")

def init_food_price_for_all_markets():
    wrapped_send(NETWORK, "STARKNET_PRIVATE_KEY", "game", "init_food_price_for_all_markets", [num_food_options])
    #out = call_or_invoke("game", "call", "get_food_price", [0,0], NETWORK)
    # print(f"get 0: {out}")

def set_player_choices_for_the_round(round_num):

    # outputs: [0, 0, 0, 1, 1, 1, 2, 2, 2] for round 0
    #for i in range(num_players):
    #    print(MarketID[Choices[i][round_num]])
    choices_list = [MarketID[Choices[i][round_num]] for i in range(num_players)]
    choices_list.insert(0,num_players)
    print(choices_list)

    #print(type(choices_list))
    #choices_str = ','.join(str(e) for e in choices_list)
    #print(f'{type(choices_str)} : {choices_str}')

    inputs = choices_list
    inputs.insert(0, round_num)
    print(inputs)
    price = wrapped_send(NETWORK, "STARKNET_PRIVATE_KEY", "game", "set_choices_for_the_round", inputs)

def calculate_food_price(round_num):
    init_food_price_for_all_markets()
    set_player_choices_for_the_round(round_num)
    for i in range(num_food_options):
        out = call_or_invoke("game", "call", "calculate_food_price", [i,0], NETWORK)
        print(f"purchase price for {i} : {out}")

def commit_auction(round_num):
    choices_list = [MarketID[Choices[i][round_num]] for i in range(num_players)]
    choices_list.insert(0,num_players)
    inputs = choices_list
    inputs.insert(0, round_num)
    print(inputs)
    price = wrapped_send(NETWORK, "STARKNET_PRIVATE_KEY", "game", "commit_auction", inputs)

def check_cumulative_units_purchased_food_price():
    wrapped_send(NETWORK, "STARKNET_PRIVATE_KEY", "game", "set_food_sold", [0, 0, 4])
    wrapped_send(NETWORK, "STARKNET_PRIVATE_KEY", "game", "set_food_sold", [0, 1, 5])
    wrapped_send(NETWORK, "STARKNET_PRIVATE_KEY", "game", "set_food_sold", [0, 2, 6])
    out = call_or_invoke("game", "call", "calculate_cumulative_units_purchased", [0,2], NETWORK)
    print(out)

# print(type(MarketID['B']))
# def misc_functions(): # ignore this function for now.
#     for i in range(num_food_options):
#         wrapped_send(NETWORK, "STARKNET_PRIVATE_KEY", "game", "set_food_sold", [i, 5+i])
#     wrapped_send(NETWORK, "STARKNET_PRIVATE_KEY", "game", "set_last_calculated_price", [1, 10])
#     price = call_or_invoke("game", "call", "get_last_calculated_price", [1], NETWORK); print(price)

if __name__ == "__main__":
    # args = sys.argv
    # if len(sys.argv) > 1:
    #    globals()[args[1]](*args[2:])
    print("hello world")
