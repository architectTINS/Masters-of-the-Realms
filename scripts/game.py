#!./bin/python

#import click
import sys
import logging

from library import wrapped_send
from nile.core.call_or_invoke import call_or_invoke


network = "localhost"
logging.basicConfig(level=logging.DEBUG, format="%(message)s")
#logging.basicConfig(level=logging.INFO, format="%(message)s")

marketid = {'R':1, 'G':2, 'B': 3}

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

def get_number_of_markets():
    """
    Get number of markets.
    """
    num_markets = call_or_invoke("game", "call", "get_number_of_markets", None, network)
    # logging.info(f'Number of markets: {num_markets}')
    return int(num_markets)

def initialisa_markets():
    num = get_number_of_markets()
    for i in range(num):
        wrapped_send(network, "STARKNET_PRIVATE_KEY", "game", "set_units_sold", [i, 5+i])
    wrapped_send(network, "STARKNET_PRIVATE_KEY", "game", "set_last_calculated_price", [1, 10])
    price = call_or_invoke("game", "call", "get_last_calculated_price", [1], network); print(price)

def initialise_players():
    num = get_number_of_players()
    for i in range(num):
        wrapped_send(network, "STARKNET_PRIVATE_KEY", "game", "get_energy_units_bought")

def set_player_choices_for_the_round(round_num):

    # outputs: [1, 1, 1, 2, 2, 2, 3, 3, 3] for round 0
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
    price = call_or_invoke("game", "call", "set_choices_for_the_round", inputs, network); print(price)

def init_pearls_for_all_players():
    out = wrapped_send(network, "STARKNET_PRIVATE_KEY", "game", "init_pearls_for_all_players", [num_players])
    print(f"sent: {out}")
    out = call_or_invoke("game", "call", "get_pearls_balance", [3,0], network)
    print(f"get 3: {out}")
    out = call_or_invoke("game", "call", "get_pearls_balance", [2,0], network)
    print(f"get 2: {out}")
    wrapped_send(network, "STARKNET_PRIVATE_KEY", "game", "set_pearls_balance", [2, 0, 51000])
    out = call_or_invoke("game", "call", "get_pearls_balance", [2,0], network)
    print(f"get 2: {out}")
    out = call_or_invoke("game", "call", "test_get_balance", None, network)
    print(f"test: {out}")
    #out = call_or_invoke("game", "call", "init_pearls_for_all_players", [num_players], network)
    #print(out)


def main():
    #create_keys()
    #initialisa_markets()
    #print(type(marketid['B']))
    #set_player_choices_for_the_round(1)
    init_pearls_for_all_players()


if __name__ == "__main__":
    # args = sys.argv
    # if len(sys.argv) > 1:
    #    globals()[args[1]](*args[2:])
    main()
    print("hello world")
