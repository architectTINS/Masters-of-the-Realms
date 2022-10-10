#!./bin/python

#import click
import sys
import logging

from starknet_wrapper import wrapped_send
from nile.core.call_or_invoke import call_or_invoke
import game_library as lib

logging.basicConfig(level=logging.DEBUG, format="%(message)s")
#logging.basicConfig(level=logging.INFO, format="%(message)s")


def main():
    lib.init_pearls_for_all_players()
    lib.init_food_price_for_all_markets()
    lib.calculate_food_price(0)
    # commit_auction(0)


if __name__ == "__main__":
    main()
    print("hello world")
