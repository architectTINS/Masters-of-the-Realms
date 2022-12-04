#!./bin/python

from constants import NETWORK
from game_data import MarketID, Choices, Market_icons
import logging
from sarayulib.cmd.invoke import invoke_function as invoke
from sarayulib.cmd.call import call_function as call

def get_number_of_players():
    """
    Get number of players.
    """
    num_players = call("game", "get_number_of_players")
    # logging.info(f'Number of players: {num_players}')
    return int(num_players)

def get_number_of_food_options():
    """
    Get number of food options.
    """
    num = call("game", "get_number_of_food_options")
    # logging.info(f'Number of food options: {num}')
    return int(num)

def get_number_of_rounds():
    """
    Get number of rounds in the game.
    """
    num = call("game", "get_number_of_rounds")
    # logging.info(f'Number of rounds: {num}')
    return int(num)


## Globals used by the functions.
num_players = get_number_of_players()
num_food_options = get_number_of_food_options()
num_rounds = get_number_of_rounds()

invMarketID = {v: k for k,v in MarketID.items()}

def init_pearls_for_all_players():
    invoke("game", "init_pearls_for_all_players", [num_players])
    #wrapped_send(NETWORK, "STARKNET_PRIVATE_KEY", "game", "init_pearls_for_all_players", [num_players])

def init_food_data_for_all_options():
    invoke("game", "init_food_data_for_all_options", [num_food_options])

def reset_food_options_demand():
    invoke("game", "reset_food_options_demand", [3])

def reset_game_state():
    invoke("game", "reset_game_state", [0])


def get_food_sold(option_id, round_num):
    out = call("game", "get_food_sold", [option_id, round_num])
    #out = call_or_invoke("game", "call", "get_food_sold", [option_id, round_num], NETWORK)
    return(int(out))

def get_food_price(option_id, round_num):
    out = call("game", "get_food_price", [option_id, round_num])
    return(int(out))

def get_food_options_demand(option_id):
    out = call("game", "get_food_options_demand", [option_id])
    return(int(out))

def get_pearls_balance(player_id, round_num):
    out = call("game", "get_pearls_balance", [player_id, round_num])
    return(int(out))

def get_latest_round(player_id, round_num):
    out = call("game", "get_latest_round")
    return(int(out))

def cumulative_food_sold(option_id, round_num):
    out = call("game", "calculate_cumulative_units_purchased", [option_id, round_num])
    return(int(out))


def set_choices_for_the_round(round_num):
    try:
        assert round_num > 0, "Assert: day cannot be less than 0."
        assert round_num <= 10, "Assert: day cannot be more than 10."
    except AssertionError as msg:
        logging.warning(msg)
        return(0)

    # outputs: [1, 1, 1, 2, 2, 2, 3, 3, 3] for round 1
    #for i in range(num_players):
    #    print(MarketID[Choices[i][round_num-1]])
    choices_list_rgb = [Choices[i][round_num-1] for i in range(num_players)]
    logging.info(f'Food choices to be set for day {round_num}: {choices_list_rgb}\n')
    choices_list_123 = [MarketID[Choices[i][round_num-1]] for i in range(num_players)]
    #logging.info(f'Food choices to be set for day {round_num}: {choices_list_123}\n')
    choices_list_123.insert(0,num_players)

    #print(type(choices_list))
    #choices_str = ','.join(str(e) for e in choices_list)
    #print(f'{type(choices_str)} : {choices_str}')

    price = invoke("game", "set_choices_for_the_round", choices_list_123)

def calculate_food_price(round_num):
    out = []
    for i in range(num_food_options):
        x = call("game", "calculate_food_price", [i+1, round_num])
        out.insert(i,x)
    return(out)

def commit_food_order(round_num):
    choices_list = [MarketID[Choices[i][round_num-1]] for i in range(num_players)]
    choices_list.insert(0,num_players)
    inputs = choices_list
    inputs.insert(0, round_num)
    #logging.info(f'Food choices to be commited for round {round_num}: {inputs}\n')
    res = invoke("game", "commit_food_order", inputs)
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
        y = invMarketID[i+1] + ":" + str(x)
        out.insert(i,y)

    return (out)

def get_food_sold_for_all_options(round):
    out = []
    for i in range(num_food_options):
        x = get_food_sold(i+1, round)
        y = invMarketID[i+1] + ":" + str(x)
        out.insert(i,y)

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
        y = invMarketID[i+1] + ":" + str(x)
        out.insert(i,y)

    return (out)

def get_food_sold_for_all_rounds(option):
    out = []
    for i in range(num_rounds):
        x = get_food_sold(option, i+1)
        out.insert(i,x)

    return (out)

def get_food_price_for_all_rounds(option):
    out = []
    for i in range(num_rounds):
        x = get_food_price(option, i+1)
        out.insert(i,x)

    return (out)

def get_pearls_balance_for_all_rounds(option):
    out = []
    for i in range(num_rounds):
        x = get_pearls_balance(option, i+1)
        out.insert(i,x)

    return (out)

def get_game_data_after_a_round(round):
    logging.info(f' >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    logging.info(f' Food prices           for day {round} 🍎 in each market [R,G,B] : {get_food_price_for_all_options(round)} pearls')
    logging.info(f' Quantity sold         for day {round} 🥗 in each market [R,G,B] : {get_food_sold_for_all_options(round)}')
    logging.info(f' Cumulative food sold till day {round} 🫐 in each market [R,G,B] : {get_cumulative_food_sold_for_all_options(round)}')
    logging.info(f' Player [P1-P9] Balance 💵 after                   day   {round} : {get_pearls_balance_for_all_players(round)} pearls')
    logging.info(f' >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

def get_demand_vs_pricing_data_for_all_rounds():
    logging.info(f'\n\n>>> Food price and sold quantity every day for each of the markets...')
    for i in range(num_food_options):
        option_id = i+1
        logging.info(f'Quantity sold in market {invMarketID[option_id]} {Market_icons[option_id]} every day : {get_food_sold_for_all_rounds(option_id)}')
        logging.info(f'Unit price in market    {invMarketID[option_id]} 💴 every day : {get_food_price_for_all_rounds(option_id)} pearls\n')

def get_player_data_for_all_round():
    logging.info(f'\n\n>>> Balances 💶 for every player after each day 📆 ...')
    logging.info(f'This may take a while. Please wait... ⏳⏳⏳')
    for i in range(num_players):
        player_id = i + 1
        logging.info(f'Player {player_id} balance after every day : {get_pearls_balance_for_all_rounds(player_id)} pearls')

def declare_winner():
    out = get_pearls_balance_for_all_players(num_rounds)
    max_value = max(out)
    max_index = out.index(max_value)
    logging.info(f'\n\n>>>> 🚀🎆💰 The WINNER_OF_THE_GAME is Player {max_index+1} ending with balance of {max_value} pearls 🎌')

    min_value = min(out)
    min_index = out.index(min_value)
    logging.info(f'\n>>>> 💸😞 Player {min_index+1} spent the most with ending balance of {min_value} pearls')

# print(type(MarketID['B']))
# def misc_functions(): # ignore this function for now.
#     for i in range(num_food_options):
#         invoke("game", "set_food_sold", [i, 5+i])
#     invoke("game", "set_last_calculated_price", [1, 10])
#     price = call("game", "get_last_calculated_price", [1]); print(price)

if __name__ == "__main__":
    # args = sys.argv
    # if len(sys.argv) > 1:
    #    globals()[args[1]](*args[2:])
    print("hello world")
