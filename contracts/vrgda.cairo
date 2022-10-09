%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin
from starkware.starknet.common.syscalls import get_block_timestamp
from starkware.cairo.common.uint256 import Uint256
from libext.math64x61 import (
    Math64x61_toUint256,
    Math64x61_add,
    Math64x61_sub,
    Math64x61_mul,
    Math64x61_div,
    Math64x61_pow,
    Math64x61_fromFelt,
    Math64x61_ONE

)

// decay rate: The price decay is k per unit of time, with no sales.
@storage_var
func decayRate() -> (res: felt) {
}

// auction start time: sn
@storage_var
func startTime() -> (res: felt) {
}

@storage_var
func unitsSoldTillNow() -> (res: felt) {
}

const UNITS_SCHEDULE = 60;
const TARGET_PRICE = 50;


@external
func purchase_price{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    requested_units: felt
) -> (res:Uint256) {
    alloc_locals;

    let (local auction_start_time) = startTime.read();
    let (local sold_till_now) = unitsSoldTillNow.read();
    let (local decay_rate) = decayRate.read();

    let (block_timestamp) = get_block_timestamp();
    let (fixed_timestamp) = Math64x61_fromFelt(block_timestamp);
    let (time_since_start) = Math64x61_sub(fixed_timestamp, auction_start_time);

    let (expected_quantiy_to_be_sold) = Math64x61_add(sold_till_now, requested_units);
    let (n_by_r) = Math64x61_div(expected_quantiy_to_be_sold, UNITS_SCHEDULE);

    let (decay_exponent) = Math64x61_sub(time_since_start, n_by_r);
    let (decay_constant) = Math64x61_sub(Math64x61_ONE, decay_rate);
    let (decay) = Math64x61_pow(decay_constant, decay_exponent);

    let (price) = Math64x61_mul(decay_constant, decay_exponent);
    
    let (vrgda_price) = Math64x61_toUint256(price);

    return (res = vrgda_price);
}
