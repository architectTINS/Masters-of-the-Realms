#!./bin/python

from nile.core.call_or_invoke import call_or_invoke
from starknet_wrapper import wrapped_send
from constants import NETWORK
from game_data import MarketID, Choices
import logging


def get_number_of_players():
    """
    Get number of players.
    """
    num_players = call_or_invoke("game", "call", "get_number_of_players", None, NETWORK)
    # logging.info(f'Number of players: {num_players}')
    return int(num_players)

def get_number_of_food_options():
    """
    Get number of food options.
    """
    num = call_or_invoke("game", "call", "get_number_of_food_options", None, NETWORK)
    # logging.info(f'Number of food options: {num}')
    return int(num)

def get_number_of_rounds():
    """
    Get number of rounds in the game.
    """
    num = call_or_invoke("game", "call", "get_number_of_rounds", None, NETWORK)
    # logging.info(f'Number of rounds: {num}')
    return int(num)


## Globals used by the functions.
num_players = get_number_of_players()
num_food_options = get_number_of_food_options()


def init_pearls_for_all_players():
    wrapped_send(NETWORK, "STARKNET_PRIVATE_KEY", "game", "init_pearls_for_all_players", [num_players])

def init_food_data_for_all_options():
    wrapped_send(NETWORK, "STARKNET_PRIVATE_KEY", "game", "init_food_data_for_all_options", [num_food_options])

def reset_foot_options_demand():
    wrapped_send(NETWORK, "STARKNET_PRIVATE_KEY", "game", "reset_foot_options_demand", [3])

def reset_game_state():
    wrapped_send(NETWORK, "STARKNET_PRIVATE_KEY", "game", "reset_game_state", [0])


def get_food_sold(option_id, round_num):
    out = call_or_invoke("game", "call", "get_food_sold", [option_id, round_num], NETWORK)
    return(int(out))

def get_food_price(option_id, round_num):
    out = call_or_invoke("game", "call", "get_food_price", [option_id, round_num], NETWORK)
    return(int(out))

def get_food_options_demand(option_id):
    out = call_or_invoke("game", "call", "get_food_options_demand", [option_id], NETWORK)
    return(int(out))

def get_pearls_balance(player_id, round_num):
    out = call_or_invoke("game", "call", "get_pearls_balance", [player_id, round_num], NETWORK)
    return(int(out))

def get_latest_round(player_id, round_num):
    out = call_or_invoke("game", "call", "get_latest_round", None, NETWORK)
    return(int(out))

def cumulative_food_sold(option_id, round_num):
    out = call_or_invoke("game", "call", "calculate_cumulative_units_purchased", [option_id, round_num], NETWORK)
    return(int(out))


def set_choices_for_the_round(round_num):
    try:
        assert round_num > 0, "Assert: round cannot be less than 0."
        assert round_num <= 10, "Assert: round cannot be more than 10."
    except AssertionError as msg:
        logging.warning(msg)
        return(0)

    # outputs: [1, 1, 1, 2, 2, 2, 3, 3, 3] for round 1
    #for i in range(num_players):
    #    print(MarketID[Choices[i][round_num-1]])
    choices_list = [MarketID[Choices[i][round_num-1]] for i in range(num_players)]
    choices_list.insert(0,num_players)
    logging.info(f'Food choices to be set for round {round_num}: {choices_list}\n')

    #print(type(choices_list))
    #choices_str = ','.join(str(e) for e in choices_list)
    #print(f'{type(choices_str)} : {choices_str}')

    price = wrapped_send(NETWORK, "STARKNET_PRIVATE_KEY", "game", "set_choices_for_the_round", choices_list)

def calculate_food_price(round_num):
    out = []
    for i in range(num_food_options):
        x = call_or_invoke("game", "call", "calculate_food_price", [i+1, round_num], NETWORK)
        out.insert(i,x)
    return(out)

def commit_food_order(round_num):
    choices_list = [MarketID[Choices[i][round_num-1]] for i in range(num_players)]
    choices_list.insert(0,num_players)
    inputs = choices_list
    inputs.insert(0, round_num)
    logging.info(f'Food choices to be set for round {round_num}: {inputs}\n')
    res = wrapped_send(NETWORK, "STARKNET_PRIVATE_KEY", "game", "commit_food_order", inputs)
    return(res)


def get_food_options_demand_for_all_options():
    out = []
    for i in range(num_food_options):
        x = get_food_options_demand(i+1)
        out.insert(i, x)

    return(out)

def get_food_price_for_all_options(round):
    out = []
    for i in range(num_food_options):
        x = get_food_price(i+1, round)
        out.insert(i,x)

    return (out)

def get_food_sold_for_all_options(round):
    out = []
    for i in range(num_food_options):
        x = get_food_sold(i+1, round)
        out.insert(i,x)

    return (out)

def get_pearls_balance_for_all_players(round):
    out = []
    for i in range(num_players):
        x = get_pearls_balance(i+1, round)
        out.insert(i,x)

    return (out)

def get_cumulative_food_sold_for_all_options(round):
    out = []
    for i in range(num_food_options):
        x = cumulative_food_sold(i+1, round)
        #x = call_or_invoke("game", "call", "calculate_cumulative_units_purchased", [i+1, round], NETWORK)
        out.insert(i,x)

    return (out)

def get_game_data_after_a_round(round):
    logging.info(f' Food prices        for round {round} : {get_food_price_for_all_options(round)}')
    logging.info(f' Food sold          for round {round} : {get_food_sold_for_all_options(round)}')
    logging.info(f' Player Balance after   round {round} : {get_pearls_balance_for_all_players(round)}')
    logging.info(f' Food sold         till round {round} : {get_cumulative_food_sold_for_all_options(round)}')

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
