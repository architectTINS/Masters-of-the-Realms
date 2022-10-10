%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin
from starkware.cairo.common.uint256 import Uint256
from libext.math import felt_to_uint256
from libext.math64x61 import (
    Math64x61_fromFelt, Math64x61_toUint256,
    Math64x61_add, Math64x61_sub, Math64x61_mul, Math64x61_div,
    Math64x61_pow,
    Math64x61_ONE
)
from openzeppelin.security.safemath.library import SafeUint256
from contracts.constants import Game

// VRGDA Formula:
// vrgda_n(t) = p0 * (1-k)^(t-s_n)
// s_n in this linear case is n/r.
// p0 = Target price.
// k = decay rate
// t = round_num + 1 = 1 to 10 = after 1 hour, 2 hours, 3 hours, etc.
//   - After 1 hour --> t = 1, round_num = 0
// n = cumulative number of NFTs/units sold by the end of this hour = sold till last hour/round + demand for this hour.
// r = UNITS_SCHEDULE = NFTs/units expected to be sold in an hour.


@external
func vrgda_price{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    p0: felt,
    k100: felt,
    t: felt,
    n: felt,
    r: felt
) -> (price: Uint256) {

    alloc_locals;

    let (_n) = Math64x61_fromFelt(n);
    let (_r) = Math64x61_fromFelt(r);
    let (local n_by_r) = Math64x61_div(_n, _r); // n/r
    //let n_by_r = n/r; // n/r

    let (_t) = Math64x61_fromFelt(t);

    let (decay_exponent) = Math64x61_sub(_t, n_by_r); // t - n/r

    let (_k100) = Math64x61_fromFelt(k100);
    let (_den100) = Math64x61_fromFelt(100);
    let (local decay_rate) = Math64x61_div(_k100, _den100); // k as %

    let (decay_constant) = Math64x61_sub(Math64x61_ONE, decay_rate); // 1-k
    let (local decay) = Math64x61_pow(decay_constant, decay_exponent); // (1-k) ^ (t - n/r)

    let (_p0) = Math64x61_fromFelt(p0);
    let (local pprice) = Math64x61_mul(p0, decay); // vrgda_n(t) = p0 * (1-k)^(t-s_n)
    
    let (vrgda_pice) = Math64x61_toUint256(pprice);

    // //return (price = vrgda_price);
    // let (_n) = felt_to_uint256(n);
    // let (_r) = felt_to_uint256(r);

    // //let (res_uint256, x) = SafeUint256.div_rem(_n, _r);
    // let (res) = Math64x61_div(n, r);
    // let (res_uint256) = Math64x61_toUint256(res);

    return (price = vrgda_pice);
}
