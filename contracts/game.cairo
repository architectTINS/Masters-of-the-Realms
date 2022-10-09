%lang starknet

from contracts.constants import Game
from starkware.cairo.common.math import assert_lt
//from starkware.cairo.common.uint256 import Uint256
//from libext.math import felt_to_uint256
from starkware.cairo.common.registers import get_fp_and_pc

from starkware.cairo.common.cairo_builtins import HashBuiltin

//struct EnergyUnitsSpent {
//    round: felt,
//    energy_units: felt,
//}

// <--- Storage variables --->
@storage_var
func units_sold_till_now(market_id: felt) -> (res: felt) {
}

@storage_var
func last_calculated_price(market_id: felt) -> (res: felt) {
}

@storage_var
func market_demand(market_id: felt, round_num: felt) -> (res: felt) {
}


@storage_var
func pearls_balance(user_id: felt, round: felt) -> (res: felt) {
}

@storage_var
func energy_units_bought(user_id: felt, round: felt) -> (res: felt) {
}


//@constructor
//func constructor{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr
//} () {
//    return();
//}


// <--- externals --->

// Energy unit sold by the market till now.
@external
func set_units_sold{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    market_id: felt, units: felt
) {
    assert_lt(market_id, Game.NUMBER_OF_MARKETS);
    units_sold_till_now.write(market_id, units);
    return();
}

@external
func set_last_calculated_price{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    market_id: felt, units: felt
) {
    assert_lt(market_id, Game.NUMBER_OF_MARKETS);
    last_calculated_price.write(market_id, units);
    return();
}

@external
func set_market_demand{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    market_id: felt, round_num: felt, new_demand: felt
) {
    assert_lt(market_id, Game.NUMBER_OF_MARKETS);
    market_demand.write(market_id, round_num, new_demand);
    return ();
}

@external
func inc_market_demand{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    market_id: felt, round_num: felt
) {
    assert_lt(market_id, Game.NUMBER_OF_MARKETS);
    let (demand) = market_demand.read(market_id, round_num);
    set_market_demand(market_id, round_num, demand+1);
    return ();
}

@external
func set_pearls_balance{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    user_id: felt, round: felt, pearls: felt
) {
    pearls_balance.write(user_id, round, pearls);
    return ();
}

// == Getters ==
// <--- views --->
@view
func get_number_of_markets{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
) -> (num_players: felt) {
    return(Game.NUMBER_OF_MARKETS,);
}

@view
func get_units_sold{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    market_id: felt) -> (res: felt) {

    assert_lt(market_id, Game.NUMBER_OF_PLAYERS);
    let (units) = units_sold_till_now.read(market_id);
    return(res=units,);
}

@view
func get_last_calculated_price{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
   market_id: felt) -> (res: felt) {

   assert_lt(market_id, Game.NUMBER_OF_PLAYERS);
   let units = last_calculated_price.read(market_id);
   return units;
}

@view
func get_number_of_players{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
) -> (num_players: felt) {
    return(Game.NUMBER_OF_PLAYERS,);
}

@view
func get_market_demand{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    market_id: felt, round_num: felt
) -> (res: felt){
    assert_lt(market_id, Game.NUMBER_OF_MARKETS);
    let (demand) = market_demand.read(market_id, round_num);
    return (res=demand);
}

@view
func get_pearls_balance{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    user_id: felt, round: felt
) -> (res: felt) {
    let (pearls) = pearls_balance.read(user_id, round);
    return (res=pearls);
}

@view
func get_energy_units_bought{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    user_id: felt, round: felt
) -> (res: felt) {
    energy_units_bought.write(user_id, round, 2);
    let (eu) = energy_units_bought.read(user_id, round);
    return(res=eu,);
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

    local market_id = in_choices[in_choices_len-1];
    inc_market_demand(market_id, round_num);

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
