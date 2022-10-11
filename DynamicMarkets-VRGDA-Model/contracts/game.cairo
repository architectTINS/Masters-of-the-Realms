%lang starknet

from contracts.constants import Game
from contracts.vrgda import vrgda_price
from starkware.cairo.common.math import assert_lt, assert_le
from starkware.cairo.common.uint256 import Uint256
//from libext.math import felt_to_uint256
from starkware.cairo.common.registers import get_fp_and_pc
from starkware.cairo.common.cairo_builtins import HashBuiltin
from libext.math64x61 import (
    Math64x61_add,      Math64x61_sub,
    Math64x61_fromFelt, Math64x61_toFelt,
    Math64x61_fromUint256
)

// ----------------------------------------------------------------------------
// <--- Storage variables --->
// Each food option sold till the round.
@storage_var
func food_sold(option_id: felt, round_num: felt) -> (res: felt) {
}

@storage_var
func food_price(option_id: felt, round_num: felt) -> (res: felt) {
}

// food_options_demand storage variable is to collect the demand for different food options.
// This is before buying food for a particular round.
//
// After food is bought, food_price will have these same values for the round.
// food_options_demand is update for each round and is not tied to
// any particular round.
// Updated by set_choices_for_the_round function.
@storage_var
func food_options_demand(option_id: felt) -> (res: felt) {
}

@storage_var
func pearls_balance(user_id: felt, round: felt) -> (res: felt) {
}

// To keep track of the last completed round number/hour.
@storage_var
func latest_round() -> (res: felt) {
}

@storage_var
func are_choices_set() -> (res: felt) {
}

// ----------------------------------------------------------------------------

// <--- externals --->

// <--- setters --->
@external
func set_food_sold{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    option_id: felt, round_num: felt, units: felt
) {
    assert_le(option_id, Game.NUMBER_OF_FOOD_OPTIONS);
    food_sold.write(option_id, round_num, units);
    return();
}

@external
func set_food_price{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    option_id: felt, round_num: felt, units: felt
) {
    assert_le(option_id, Game.NUMBER_OF_FOOD_OPTIONS);
    food_price.write(option_id, round_num, units);
    return();
}

@external
func set_food_options_demand{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    option_id: felt, new_demand: felt
) {
    assert_le(option_id, Game.NUMBER_OF_FOOD_OPTIONS);
    food_options_demand.write(option_id, new_demand);
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
// ----------------------------------------------------------------------------

// <--- Increment function --->
@external
func inc_food_sold{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    option_id: felt, round_num: felt
) {
    assert_le(option_id, Game.NUMBER_OF_FOOD_OPTIONS);
    let (prev_units) = food_sold.read(option_id, round_num);
    food_sold.write(option_id, round_num, prev_units + 1);
    return();
}
@external
func inc_food_options_demand{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    option_id: felt
) {
    assert_le(option_id, Game.NUMBER_OF_FOOD_OPTIONS);
    let (demand) = food_options_demand.read(option_id);
    set_food_options_demand(option_id, demand + 1);
    return ();
}
// ----------------------------------------------------------------------------

// < Getters/views ==
// <--- views --->

@view
func get_food_sold{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    option_id: felt, round_num: felt) -> (res: felt) {

    assert_le(option_id, Game.NUMBER_OF_PLAYERS);
    let (units) = food_sold.read(option_id, round_num);
    return(res=units,);
}

@view
func get_food_price{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
   option_id: felt, round_num: felt) -> (res: felt) {

   assert_le(option_id, Game.NUMBER_OF_PLAYERS);
   let units = food_price.read(option_id, round_num);
   return units;
}

@view
func get_food_options_demand{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    option_id: felt
) -> (res: felt){
    assert_le(option_id, Game.NUMBER_OF_FOOD_OPTIONS);
    let (demand) = food_options_demand.read(option_id);
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
// ----------------------------------------------------------------------------
@view
func get_number_of_players{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
) -> (num_players: felt) {
    return(Game.NUMBER_OF_PLAYERS,);
}

@view
func get_number_of_food_options{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
) -> (num_players: felt) {
    return(Game.NUMBER_OF_FOOD_OPTIONS,);
}

@view
func get_number_of_rounds{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
) -> (num_players: felt) {
    return(Game.NUMBER_OF_ROUNDS,);
}
// ----------------------------------------------------------------------------

// @view
// func test_array{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
//     len: felt
// ) -> (res_len: felt, res: felt*) {

//     alloc_locals;
//     let (__fp__, _) = get_fp_and_pc();

//     let (pearls) = pearls_balance.read(1,1);

//     local num: (felt, felt, felt) = (pearls,2,3);
//     return(res_len=3, res=&num);
// }
// // ----------------------------------------------------------------------------

@external
func init_pearls_for_all_players{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    player_id: felt
) -> () {

    alloc_locals;

    let round = 0;
    let balance = Game.INITIAL_PEARL_BALANCE;

    if (player_id == 0) {
        return ();
    } else {
        init_pearls_for_all_players(player_id-1);
    }

    pearls_balance.write(player_id, round, balance);

    return ();
}

@external
func init_food_data_for_all_options{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    option_id: felt
) -> () {
    alloc_locals;

    let round = 0;
    let price = Game.INITIAL_FOOD_PRICE;

    if(option_id == 0) {
        return ();
    } else {
        init_food_data_for_all_options(option_id-1);
    }

    food_price.write(option_id, round, price);
    food_sold.write(option_id, round, 0);

    return();
}

@external
func reset_food_options_demand{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    option_id: felt
) -> () {

    food_options_demand.write(option_id, 0);

    if(option_id == 0) {
        return ();
    } else {
        reset_food_options_demand(option_id - 1);
    }

    are_choices_set.write(0);

    return();
}

@external
func reset_game_state{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    reset_data: felt
) {
    latest_round.write(0);
    return();
}
// ----------------------------------------------------------------------------

// Set food choices of all the players for the given round.
func set_food_options_demand_for_the_round{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    in_choices_len: felt, in_choices: felt*
) -> () {

    alloc_locals;

    if(in_choices_len == 0) {
        return();
    } else {
        set_food_options_demand_for_the_round(in_choices_len-1, in_choices);
    }

    local option_id = in_choices[in_choices_len-1];
    inc_food_options_demand(option_id);

    return ();
}

// Reset and call function to set food choices of all the players for the given round.
@external
func set_choices_for_the_round{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    in_choices_len: felt, in_choices: felt*
) -> () {

    reset_food_options_demand(Game.NUMBER_OF_FOOD_OPTIONS);

    set_food_options_demand_for_the_round(in_choices_len, in_choices);

    are_choices_set.write(1);

    return ();
}

// Calculate the food option sold till round_num.
@view
func calculate_cumulative_units_purchased{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    option_id: felt, round_num: felt
) -> (res: felt){

    if (round_num == 0) {
        return (res=0);
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

    let (price) = food_price.read(option_id, 0); // price before the start of the game - round 0.

    // Assigning in a new variable to fix this error.
    // contracts/game.cairo:299:29: Reference 'p0' was revoked. - let (res) = vrgda_price(p0, k100, t, n, r);
    let p0 = price;
    let k100 = Game.DECAY_PERCENTAGE;
    let t = round_num;

    let (units_till_now) = calculate_cumulative_units_purchased(option_id, round_num-1);
    let (demand) = food_options_demand.read(option_id);
    let n = units_till_now + demand;

    let r = Game.UNITS_SCHEDULE;

    let (res) = vrgda_price(p0, k100, t, n, r);

    return(res=res);
}

func update_selling_price_for_all_options{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    option_id: felt, round_num: felt
) -> (){

    if (option_id == 0) {
        return ();
    } else {
        update_selling_price_for_all_options(option_id-1, round_num);
    }

    let (price) = calculate_food_price(option_id, round_num);
    // Update purchase price for the market for this round.
    food_price.write(option_id, round_num, price.low);

    return ();
}

func update_food_sold{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr} (
    option_id: felt, round_num: felt
) {

    if (option_id == 0) {
        return ();
    } else {
        update_food_sold(option_id-1, round_num);
    }

    let (x) = get_food_options_demand(option_id);
    set_food_sold(option_id, round_num, x);

    return ();
}

func pay_pearls{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    round_num: felt, in_choices_len: felt, in_choices: felt*
) {

    alloc_locals;

    if (in_choices_len == 0) {
        return ();
    } else {
        pay_pearls(round_num, in_choices_len-1, in_choices);
    }

    local option_id = in_choices[in_choices_len-1];
    local player_id   = in_choices_len;

    let (price) = calculate_food_price(option_id,round_num);
    let (previous_balance) = pearls_balance.read(player_id, round_num-1);

    // update pearls balance for this round for each player.
    let (_price) = Math64x61_fromUint256(price);
    let (_prev_balance) = Math64x61_fromFelt(previous_balance);
    let (_new_balance) = Math64x61_sub(_prev_balance, _price);
    let (new_balance) = Math64x61_toFelt(_new_balance);
    pearls_balance.write(player_id, round_num, new_balance);

    return ();
}

// Inputs:
//   1. Round number
//   2. Choices for each player i.e. market ids of the markets they are going to buy Energy units from.
@external
func commit_food_order{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    round_num: felt, in_choices_len: felt, in_choices: felt*
) -> (res: felt) {
    alloc_locals;

    // Invalid choices cannot be commited.
    if (in_choices_len == 0) {
        return (res=0);
    }

    assert_le(round_num, Game.NUMBER_OF_ROUNDS);

    // Choices are not set yet. No point in processing the order.
    let (choices_set) = are_choices_set.read();
    if(choices_set == 0) {
        return (res=0);
    }

    // Check to make sure orders of the previous rounds are not amended.
    let (latest) = latest_round.read();
    assert_lt(latest, round_num);

    // Update purchase price for the market for this round.
    update_selling_price_for_all_options(Game.NUMBER_OF_FOOD_OPTIONS, round_num);

    // Update Units sold in this round.
    update_food_sold(Game.NUMBER_OF_FOOD_OPTIONS, round_num);

    // update pearls balance for this round for each player.
    pay_pearls(round_num, in_choices_len, in_choices);

    // keep track of latest round.
    latest_round.write(round_num);

    // reset the choices made for this round.
    reset_food_options_demand(Game.NUMBER_OF_FOOD_OPTIONS);

    return (res=1);
}