#!./bin/python

#import click
import sys
import logging

from library import wrapped_send
from nile.core.call_or_invoke import call_or_invoke


network = "localhost"
logging.basicConfig(level=logging.DEBUG, format="%(message)s")
#logging.basicConfig(level=logging.INFO, format="%(message)s")

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

def main():
    #create_keys()
    initialisa_markets()

if __name__ == "__main__":
    # args = sys.argv
    # if len(sys.argv) > 1:
    #    globals()[args[1]](*args[2:])
    main()
    print("hello world")
