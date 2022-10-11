# This file is taken from realm-contracts.

# First, import click dependency
import click

import re
import subprocess

from symbol import argument
from nile.core.account import Account, get_nonce
from nile import deployments
from nile.core.call_or_invoke import call_or_invoke
from constants import MAX_FEE

def send_multi(self, to, method, calldata, nonce=None):
    """Execute a tx going through an Account contract. Inspired from openzeppelin."""
    #config = Config(nile_network=self.network)

    target_address, _ = next(deployments.load(to, self.network)) or to
    #target_address, _ = next(deployments.load(to, "127.0.0.1")) or to

    # print(calldata)
    calldata = [[int(x) for x in c] for c in calldata]
    # print(calldata)

    if nonce is None:
        nonce = get_nonce(self.address, self.network)

    (execute_calldata, sig_r, sig_s) = self.signer.sign_transaction(
        sender=self.address,
        calls=[[target_address, method, c] for c in calldata],
        nonce=nonce,
        max_fee=MAX_FEE,
    )

    # params = []
    # # params.append(str(len(call_array)))
    # # params.extend([str(elem) for sublist in call_array for elem in sublist])
    # params.append(str(len(calldata)))
    # params.extend([str(param) for param in calldata])
    # params.append(str(nonce))

    # print(execute_calldata)
    #print()

    return call_or_invoke(
        contract=self.address,
        type="invoke",
        method="__execute__",
        params=execute_calldata,
        network=self.network,
        signature=[str(sig_r), str(sig_s)],
        max_fee=str(MAX_FEE),
    )

# bind it to the account class so that we can use the function when signing
Account.send_multi = send_multi

def send(network, signer_alias, contract_alias, function, arguments) -> str:
    """Nile send function."""
    #print(f"Balaji - send -- network: {network}")
    #if network == "127.0.0.1":
    #    network = "localhost"
    #    print("Network changed!!!")

    account = Account(signer_alias, network)
    if isinstance(arguments[0], list):
        return account.send_multi(contract_alias, function, arguments)
    return account.send_multi(contract_alias, function, [arguments])

def parse_send(x):
    """Extract information from send command."""
    # address is 64, tx_hash is 64 chars long
    try:
        address, tx_hash = re.findall("0x[\\da-f]{1,64}", str(x))
        return address, tx_hash
    except ValueError:
        print(f"could not get tx_hash from message {x}")
    return 0x0, 0x0

def get_tx_status(network, tx_hash: str) -> dict:
    """Returns transaction receipt in dict."""
    command = ["nile", "debug",
        "--network", network,
        tx_hash,
    ]
    out_raw = subprocess.check_output(command).strip().decode("utf-8")
    return out_raw

def wrapped_send(network, signer_alias, contract_alias, function, arguments):
    """Send command with some extra functionality such as tx status check and built-in timeout.
    (only supported for non-localhost networks)

    tx statuses:
    RECEIVED -> PENDING -> ACCEPTED_ON_L2
    """
    print("------- SEND ----------------------------------------------------")
    print(f"invoking {function} from {contract_alias} with {arguments} in {network}")
    out = send(network, signer_alias, contract_alias, function, arguments)
    if out:
        _, tx_hash = parse_send(out)
        get_tx_status(network, tx_hash,)
    else:
        raise Exception("send message returned None")
    print("------- SEND ----------------------------------------------------\n")

