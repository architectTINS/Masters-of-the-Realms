#!./bin/python

#import click
import sys
import logging

from library import wrapped_send
from nile.core.call_or_invoke import call_or_invoke


network = "localhost"
logging.basicConfig(level=logging.DEBUG, format="%(message)s")
#logging.basicConfig(level=logging.INFO, format="%(message)s")

marketid = {'R':0, 'G':1, 'B': 2}

choices = [
    ['R','R','R','R','R', 'R','R','R','R','R'],
    ['R','R','B','G','G', 'R','B','R','B','R'],
    ['R','G','R','R','R', 'R','R','G','R','B'],
    ['G','R','G','G','G', 'R','G','R','G','G'],
    ['G','B','R','B','R', 'G','R','G','G','G'],
    ['G','G','G','G','G', 'G','G','G','B','G'],
    ['B','B','B','B','B', 'R','B','B','B','B'],
    ['B','G','G','R','B', 'B','B','G','B','B'],
    ['B','R','B','B','G', 'R','B','G','R','B'],
]

def market_get_set_id():
    """
    Set and Get market id.
    """
    out = call_or_invoke("game", "call", "get_id", None, network); print(out)
    id = 180
    wrapped_send(network, "STARKNET_PRIVATE_KEY", "market", "set_id", [id])
    out = call_or_invoke("game", "call", "get_id", None, network); print(out)

def get_number_of_players():
    """
    Get number of players.
    """
    num_players = call_or_invoke("game", "call", "get_number_of_players", None, network)
    # logging.info(f'Number of players: {num_players}')
    return int(num_players)

num_players = get_number_of_players()

def get_number_of_food_options():
    """
    Get number of markets.
    """
    num = call_or_invoke("game", "call", "get_number_of_food_options", None, network)
    # logging.info(f'Number of markets: {num}')
    return int(num)

num_markets = get_number_of_food_options()

def initialise_markets(): # ignore this function for now.
    for i in range(num_markets):
        wrapped_send(network, "STARKNET_PRIVATE_KEY", "game", "set_food_sold", [i, 5+i])
    wrapped_send(network, "STARKNET_PRIVATE_KEY", "game", "set_last_calculated_price", [1, 10])
    price = call_or_invoke("game", "call", "get_last_calculated_price", [1], network); print(price)

def initialise_players():
    for i in range(num_players):
        wrapped_send(network, "STARKNET_PRIVATE_KEY", "game", "set_last_calculated_price", [1, 6]) # more arguments needed here. will not work.

def set_player_choices_for_the_round(round_num):

    # outputs: [0, 0, 0, 1, 1, 1, 2, 2, 2] for round 0
    #for i in range(num_players):
    #    print(marketid[choices[i][round_num]])
    choices_list = [marketid[choices[i][round_num]] for i in range(num_players)]
    choices_list.insert(0,num_players)
    print(choices_list)

    #print(type(choices_list))
    #choices_str = ','.join(str(e) for e in choices_list)
    #print(f'{type(choices_str)} : {choices_str}')

    inputs = choices_list
    inputs.insert(0, round_num)
    print(inputs)
    price = wrapped_send(network, "STARKNET_PRIVATE_KEY", "game", "set_choices_for_the_round", inputs)

def init_pearls_for_all_players():
    wrapped_send(network, "STARKNET_PRIVATE_KEY", "game", "init_pearls_for_all_players", [num_players])
    #out = call_or_invoke("game", "call", "get_pearls_balance", [8,0], network)
    #print(f"get 3: {out}")

def init_food_price_for_all_markets():
    wrapped_send(network, "STARKNET_PRIVATE_KEY", "game", "init_food_price_for_all_markets", [num_markets])
    out = call_or_invoke("game", "call", "get_food_price", [0,0], network)
    print(f"get 0: {out}")

def check_cumulative_units_purchased_food_price():
    wrapped_send(network, "STARKNET_PRIVATE_KEY", "game", "set_food_sold", [0, 0, 4])
    wrapped_send(network, "STARKNET_PRIVATE_KEY", "game", "set_food_sold", [0, 1, 5])
    wrapped_send(network, "STARKNET_PRIVATE_KEY", "game", "set_food_sold", [0, 2, 6])
    out = call_or_invoke("game", "call", "calculate_cumulative_units_purchased", [0,2], network)
    print(out)

def calculate_food_price(round_num):
    init_food_price_for_all_markets()
    set_player_choices_for_the_round(round_num)
    for i in range(num_markets):
        out = call_or_invoke("game", "call", "calculate_food_price", [i,0], network)
        print(f"purchase price for {i} : {out}")

def commit_auction(round_num):
    choices_list = [marketid[choices[i][round_num]] for i in range(num_players)]
    choices_list.insert(0,num_players)
    inputs = choices_list
    inputs.insert(0, round_num)
    print(inputs)
    price = wrapped_send(network, "STARKNET_PRIVATE_KEY", "game", "commit_auction", inputs)


def main():
    #create_keys()
    #initialise_markets()
    #print(type(marketid['B']))
    init_pearls_for_all_players()
    #init_food_price_for_all_markets()
    calculate_food_price(0)
    commit_auction(0)

    # update round_num when you commit to a transaction.


if __name__ == "__main__":
    # args = sys.argv
    # if len(sys.argv) > 1:
    #    globals()[args[1]](*args[2:])
    main()
    print("hello world")
