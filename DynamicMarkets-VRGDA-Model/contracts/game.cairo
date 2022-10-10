%lang starknet

from contracts.constants import Game
from contracts.vrgda import vrgda_price
from starkware.cairo.common.math import assert_lt
from starkware.cairo.common.uint256 import Uint256
//from libext.math import felt_to_uint256
from starkware.cairo.common.registers import get_fp_and_pc
from starkware.cairo.common.cairo_builtins import HashBuiltin
from libext.math64x61 import (
    Math64x61_add,      Math64x61_sub,
    Math64x61_fromFelt, Math64x61_toFelt,
    Math64x61_fromUint256
)

// <--- Storage variables --->
@storage_var
func food_sold(option_id: felt, round_num: felt) -> (res: felt) {
}

@storage_var
func food_price(option_id: felt, round_num: felt) -> (res: felt) {
}

@storage_var
func initial_food_price(option_id: felt) -> (res: felt) {
}


@storage_var
func market_demand(option_id: felt, round_num: felt) -> (res: felt) {
}


@storage_var
func pearls_balance(user_id: felt, round: felt) -> (res: felt) {
}

// To keep track of the last completed round number/hour.
@storage_var
func latest_round() -> (res: felt) {
}

// <--- externals --->

// Each food option sold till now.
@external
func set_food_sold{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    option_id: felt, round_num: felt, units: felt
) {
    assert_lt(option_id, Game.NUMBER_OF_FOOD_OPTIONS);
    food_sold.write(option_id, round_num, units);
    return();
}

@external
func inc_food_sold{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    option_id: felt, round_num: felt
) {
    assert_lt(option_id, Game.NUMBER_OF_FOOD_OPTIONS);
    let (prev_units) = food_sold.read(option_id, round_num);
    food_sold.write(option_id, round_num, prev_units + 1);
    return();
}

@external
func set_food_price{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    option_id: felt, round_num: felt, units: felt
) {
    assert_lt(option_id, Game.NUMBER_OF_FOOD_OPTIONS);
    food_price.write(option_id, round_num, units);
    return();
}

@external
func set_market_demand{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    option_id: felt, round_num: felt, new_demand: felt
) {
    assert_lt(option_id, Game.NUMBER_OF_FOOD_OPTIONS);
    market_demand.write(option_id, round_num, new_demand);
    return ();
}

@external
func inc_market_demand{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    option_id: felt, round_num: felt
) {
    assert_lt(option_id, Game.NUMBER_OF_FOOD_OPTIONS);
    let (demand) = market_demand.read(option_id, round_num);
    set_market_demand(option_id, round_num, demand + 1);
    return ();
}

@external
func set_pearls_balance{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    user_id: felt, round: felt, pearls: felt
) {
    pearls_balance.write(user_id, round, pearls);
    return ();
}

@external
func set_latest_round{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    round_num: felt
) {
    latest_round.write(round_num);
    return();
}

// == Getters ==
// <--- views --->
@view
func get_number_of_food_options{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
) -> (num_players: felt) {
    return(Game.NUMBER_OF_FOOD_OPTIONS,);
}

@view
func get_food_sold{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    option_id: felt, round_num: felt) -> (res: felt) {

    assert_lt(option_id, Game.NUMBER_OF_PLAYERS);
    let (units) = food_sold.read(option_id, round_num);
    return(res=units,);
}

@view
func get_food_price{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
   option_id: felt, round_num: felt) -> (res: felt) {

   assert_lt(option_id, Game.NUMBER_OF_PLAYERS);
   let units = food_price.read(option_id, round_num);
   return units;
}

@view
func get_initial_food_price{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
   option_id: felt) -> (res: felt) {

   assert_lt(option_id, Game.NUMBER_OF_PLAYERS);
   let units = initial_food_price.read(option_id);
   return units;
}

@view
func get_number_of_players{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
) -> (num_players: felt) {
    return(Game.NUMBER_OF_PLAYERS,);
}

@view
func get_market_demand{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    option_id: felt, round_num: felt
) -> (res: felt){
    assert_lt(option_id, Game.NUMBER_OF_FOOD_OPTIONS);
    let (demand) = market_demand.read(option_id, round_num);
    return (res=demand);
}

@view
func get_pearls_balance{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    user_id: felt, round: felt
) -> (res: felt) {
    let (pearls) = pearls_balance.read(user_id, round);
    return (res=pearls);
}

@external
func get_latest_round{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
) -> (res: felt) {
    let (round_num) = latest_round.read();
    return(res=round_num);
}

@view
func test_array{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    len: felt
) -> (res_len: felt, res: felt*) {

    alloc_locals;
    let (__fp__, _) = get_fp_and_pc();

    let (pearls) = pearls_balance.read(1,1);

    local num: (felt, felt, felt) = (pearls,2,3);
    return(res_len=3, res=&num);
}

@external
func set_choices_for_the_round{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    round_num: felt, in_choices_len: felt, in_choices: felt*
) -> () {

    alloc_locals;

    assert_lt(round_num, Game.NUMBER_OF_ROUNDS);

    if(in_choices_len == 0) {
        return();
    } else {
        set_choices_for_the_round(round_num, in_choices_len-1, in_choices);
    }

    local option_id = in_choices[in_choices_len-1];
    inc_market_demand(option_id, round_num);

    //let res = in_choices[7];
    //return (res=res);
    return ();
}

@external
func init_pearls_for_all_players{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    num: felt
) -> () {

    alloc_locals;

    let round = 0;
    let balance = Game.INITIAL_PEARL_BALANCE;

    if (num == 0) {
        return ();
    } else {
        init_pearls_for_all_players(num-1);
    }

    local player_id = num - 1;
    pearls_balance.write(player_id, round, balance);

    return ();
}

@external
func init_food_price_for_all_markets{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    num: felt
) -> () {
    alloc_locals;

    let round = 0;
    let price = Game.INITIAL_FOOD_PRICE;

    if(num == 0) {
        return ();
    } else {
        init_food_price_for_all_markets(num-1);
    }

    local option_id = num - 1;
    food_price.write(option_id, round, price);
    initial_food_price.write(option_id, price);

    return();
}

// Calculate the energy units sold in a market till round_num.
@view
func calculate_cumulative_units_purchased{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    option_id: felt, round_num: felt
) -> (res: felt){

    if (round_num == -1) {
        return (res=0);
    }

    if (round_num == 0) {
        let (units) = food_sold.read(option_id,0);
        return(res=units);
    } else {
        let (units_prev) = calculate_cumulative_units_purchased(option_id, round_num-1);
    }

    let (units_cur) = food_sold.read(option_id, round_num);
    let units = units_prev + units_cur;

    return (res=units);
}

@view
func calculate_food_price{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    option_id: felt, round_num: felt
) -> (res: Uint256) {

    alloc_locals;

    let (price) = initial_food_price.read(option_id);

    // Assigning in a new variable to fix this error.
    // contracts/game.cairo:299:29: Reference 'p0' was revoked. - let (res) = vrgda_price(p0, k100, t, n, r);
    let p0 = price;

    let k100 = Game.DECAY_PERCENTAGE;
    // Note: round 0 occurs after an hour after the start of the game. so, round_num = 0 ==> t = 1.
    let t = round_num + 1;

    let (units_till_now) = calculate_cumulative_units_purchased(option_id, round_num-1);

    let (demand) = market_demand.read(option_id, round_num);
    let n = units_till_now + demand;

    let r = Game.UNITS_SCHEDULE;

    let (res) = vrgda_price(p0, k100, t, n, r);

    return(res=res);
}

// Inputs:
//   1. Round number
//   2. Choices for each player i.e. market ids of the markets they are going to buy Energy units from.
@external
func commit_auction{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    round_num: felt, in_choices_len: felt, in_choices: felt*
) {
    alloc_locals;

    if (in_choices_len == 0) {
        return ();
    }

    assert_lt(round_num, Game.NUMBER_OF_ROUNDS);

    local option_id = in_choices[in_choices_len-1];
    local user_id = in_choices_len-1;
    
    let (price) = calculate_food_price(option_id,round_num);

    if (round_num == 0) {
        let (previous_balance) = pearls_balance.read(user_id, 0);
    } else {
        let prev_round = round_num - 1;
        let (previous_balance) = pearls_balance.read(user_id, prev_round);
    }

    // update pearls balance for this round for each player.
    let (_price) = Math64x61_fromUint256(price);
    let (_prev_balance) = Math64x61_fromFelt(previous_balance);
    let (_new_balance) = Math64x61_sub(_price, _prev_balance);
    let (new_balance) = Math64x61_toFelt(_new_balance);
    pearls_balance.write(user_id, round_num, new_balance);

    // Update Units sold in this round.
    inc_food_sold(option_id, round_num);

    // Update purchase price for the market for this round.
    food_price.write(option_id, round_num, price.low);


    // keep track of latest round.
    latest_round.write(round_num);

    return ();
}