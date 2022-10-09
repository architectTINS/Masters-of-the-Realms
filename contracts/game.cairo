%lang starknet

from contracts.constants import Game
from starkware.cairo.common.math import assert_lt
//from starkware.cairo.common.uint256 import Uint256
//from libext.math import felt_to_uint256
from starkware.cairo.common.registers import get_fp_and_pc

from starkware.cairo.common.cairo_builtins import HashBuiltin

struct EnergyUnitsSpent {
    round: felt,
    energy_units: felt,
}

// <--- Storage variables --->
@storage_var
func units_sold_till_now(market_id: felt) -> (res: felt) {
}

@storage_var
func last_calculated_price(market_id: felt) -> (res: felt) {
}

@storage_var
func market_id() -> (res: felt) {
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
func set_id{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    marketid_to_set: felt
) {
    market_id.write(marketid_to_set);
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
func get_id{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
) -> (out_id: felt) {
    let (res) = market_id.read();
    return (out_id=res);
}

@view
func get_number_of_players{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
) -> (num_players: felt) {
    return(Game.NUMBER_OF_PLAYERS,);
}

@external
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