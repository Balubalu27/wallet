import secrets
from decimal import Decimal

from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import HTTPProvider, Web3

from config.env import API_KEY, NETWORK_URL


def create_account() -> LocalAccount:
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    return Account.from_key(private_key)


def get_account_balance(address: str) -> Decimal:
    web3 = Web3(HTTPProvider(f'{NETWORK_URL}{API_KEY}'))
    return Decimal(web3.eth.get_balance(address))
