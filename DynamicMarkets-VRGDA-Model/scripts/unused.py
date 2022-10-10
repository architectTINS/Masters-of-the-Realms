# This file is a dump of the unused functions.
# This file will not work.

from ecdsa import SigningKey, SECP128r1
from ecdsa.util import PRNG

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
