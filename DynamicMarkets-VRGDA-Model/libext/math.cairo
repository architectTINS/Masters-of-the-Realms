%lang starknet

// This function is from the common library.
// It can live here, reducing the clutter of an application.
from starkware.cairo.common.math import split_felt, unsigned_div_rem
from starkware.cairo.common.uint256 import Uint256

// This function is imported by 'custom_import.cairo'
// Equivalent to placing this function in that file.
func add_two(a: felt, b: felt) -> (sum: felt) {
    let sum = a + b;
    return (sum=sum);
}

// This function performs the modulo operation.
func get_modulo{range_check_ptr}(a: felt, b: felt) -> (result: felt) {
    let (dividend, remainder) = unsigned_div_rem(a, b);

    // The dividend is not used, and the following is equivalent:
    // let (_, remainder) = unsigned_div_rem(a, b)
    return (result=remainder);
}

func felt_to_uint256{range_check_ptr}(x) -> (x_: Uint256) {
    let split = split_felt(x);
    return (Uint256(low=split.low, high=split.high),);
}