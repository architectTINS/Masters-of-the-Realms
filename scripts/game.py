#!./bin/python

#import click
import sys
import logging

from library import wrapped_send
from nile.core.call_or_invoke import call_or_invoke
from ecdsa import SigningKey, SECP128r1
from ecdsa.util import PRNG

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


def create_pk(seed):
    rng = PRNG(seed)
    sk = SigningKey.generate(entropy=rng)
    sk_string = sk.to_string()
    sk_hex = sk_string.hex();      # print(f'Hex: {sk_hex}')
    sk_int = int('0x'+sk_hex, 16); # print(sk_int)
    return sk_int

def create_keys_for_players():
    num = get_number_of_players()
    player_keys = []
    for i in range(num):
        seed = "player" + str(i)
        pk = create_pk(bytes(seed.encode('utf-8')))
        # print(f"{i} : {pk}")
        player_keys.append(pk)
    return player_keys

def create_keys_for_markets():
    num = get_number_of_markets()
    market_keys = []
    for i in range(num):
        seed = "market" + str(i)
        pk = create_pk(bytes(seed.encode('utf-8')))
        market_keys.append(pk)
    return market_keys

def create_keys():
    player_keys = create_keys_for_players()
    market_keys = create_keys_for_markets()
    for i in range(len(player_keys)):
        logging.info(f'{i} : {player_keys[i]}')
    for i in range(len(market_keys)):
        logging.info(f'{i} : {market_keys[i]}')

def initialisa_markets():
    #num = get_number_of_markets()
    #for i in range(num):
    #    wrapped_send(network, "STARKNET_PRIVATE_KEY", "game", "set_units_sold", [i, 5+i])
    wrapped_send(network, "STARKNET_PRIVATE_KEY", "game", "set_last_calculated_price", [1, 10])
    price = call_or_invoke("game", "call", "get_last_calculated_price", [1], network); print(price)

def initialise_players():
    num = get_number_of_players()
    for i in range(num):
        wrapped_send(network, "STARKNET_PRIVATE_KEY", "game", "get_energy_units_remaining")

def main():
    #create_keys()
    initialisa_markets()

if __name__ == "__main__":
    # args = sys.argv
    # if len(sys.argv) > 1:
    #    globals()[args[1]](*args[2:])
    main()
    print("hello world")
