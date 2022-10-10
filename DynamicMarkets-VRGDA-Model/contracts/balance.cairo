// Declare this file as a StarkNet contract.
// This file is just a test file. Has got nothing to do with DynamicMarkets.
%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin
from starkware.cairo.common.uint256 import Uint256

// Define a storage variable.
@storage_var
func balance() -> (res: felt) {
}

// Increases the balance by the given amount.
@external
func increase_balance{
    syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr
}(amount: felt) {
    let (res) = balance.read();
    balance.write(res + amount);
    return ();
}

// Increases the balance by the given amount.
@external
func decrease_balance{
    syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr
}(amount: felt){
    let (res) = balance.read();
    balance.write(res - amount);
    return ();
}

// Reset balance to zero
@external
func reset_balance{
    syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr
}(){
    balance.write(0);
    return ();
}

// Returns the current balance.
@view
func get_balance{
    syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr
}() -> (res: felt) {
    let (res) = balance.read();
    // or, return(res,); can be used
    return (res=res);
}

