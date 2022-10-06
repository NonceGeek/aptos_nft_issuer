# Copyright (c) Aptos
# SPDX-License-Identifier: Apache-2.0
# based on:
# > https://github.com/aptos-labs/aptos-core/tree/main/ecosystem/python/sdk

import json
import click

from aptos_sdk.account import Account
from aptos_sdk.client import FaucetClient, RestClient

from common import FAUCET_URL, NODE_URL

@click.command()
@click.option('--gen_acct',  flag_value=True, help='generate Aptos Account')
@click.option('--get_faucet',  help='--get faucet [acct]')
@click.option('--priv',  help='privkey in hex format')
@click.option('--create_collection',  help='collection informations. Example: \'["test", "hello", "www.google.com"]\'')
@click.option('--create_token',  help='token informations: Example: TODO')
@click.option('--create_tokens',  help='token informations: ')

def main(gen_acct, get_faucet, priv, create_collection, create_token, create_tokens):
    rest_client = RestClient(NODE_URL)
    faucet_client = FaucetClient(FAUCET_URL, rest_client)

    if gen_acct == True:
        #:!:>section gen acct
        user = Account.generate()
        print("\n=== Addresses ===")
        print(f"User Addr: {user.address()}")
        print(f"User Priv: {user.private_key.hex()}")
        # <:!:section gen acct
    if get_faucet != None:
        #:!:>section get faucet
        faucet_client.fund_account(get_faucet, 100_000_000)

        print("\n=== Initial Coin Balances ===")
        print(f"User: {rest_client.account_balance(get_faucet)}")
        # <:!:section get faucet

    if create_collection != None:
        #:!:>section create collection
        payload = json.loads(create_collection)
        acct = Account.load_key(priv)
        txn_hash = rest_client.create_collection(
            acct, payload[0], payload[1], payload[2]
        )  
        #  acct, collection_name, description, url
        rest_client.wait_for_transaction(txn_hash)
        print("\n=== Creating Collection and Token ===")

        collection_data = rest_client.get_collection(acct.address(), payload[0])
        print(
            f"User's collection: {json.dumps(collection_data, indent=4, sort_keys=True)}"
        )
        # <:!:section create collection

    if create_token != None:
        #:!:>section create token
        payload = json.loads(create_token)
        acct = Account.load_key(priv)
        #     # see in:
        # > https://github.com/aptos-labs/aptos-core/blob/main/aptos-move/framework/aptos-token/sources/token.move
        txn_hash = rest_client.create_token(
            acct,
            payload[0],
            payload[1],
            payload[2],
            payload[3],
            payload[4],
            0,
        ) 

        # public entry fun create_token_script(
        #     account: &signer,
        #     collection: String,
        #     name: String,
        #     description: String,
        #     balance: u64,
        #     maximum: u64,
        #     uri: String,
        #     royalty_payee_address: address,
        #     royalty_points_denominator: u64,
        #     royalty_points_numerator: u64,
        #     mutate_setting: vector<bool>,
        #     property_keys: vector<String>,
        #     property_values: vector<vector<u8>>,
        #     property_types: vector<String>
        # )    
        # Example
        #         acct,
        #         collection_name,
        #         token_name,
        #         "Alice's simple token",
        #         1,
        #         "https://aptos.dev/img/nyan.jpeg",
        #         0,
        rest_client.wait_for_transaction(txn_hash)

        token_data = rest_client.get_token_data(
            acct.address(), payload[0], payload[1], 0
        )
        print(
            f"User's token data: {json.dumps(token_data, indent=4, sort_keys=True)}"
        )
        #:!:>section create token
    # TODO: get collection info
    # TODO: get token info
    # TODO: transfer token
    # TODO: get balance
    # ↑bounty price => $ 200↑

    # ↓bounty price => $ 200↓
    # TODO: mint Multi Tokens
    # requirement: Add the ship link of Arweave/IPFS
    # mint Tokens
    if create_tokens != None:
        # Token standard: https://aptos.dev/concepts/coin-and-token/aptos-token/#storing-metadata-off-chain
        # {
        #   "image": "https://www.arweave.net/abcd5678?ext=png",
        #   "animation_url": "https://www.arweave.net/efgh1234?ext=mp4",
        #   "external_url": "https://solflare.com"
        pass

if __name__ == "__main__":
    main()
#     #:!:>section_1
#     rest_client = RestClient(NODE_URL)
#     faucet_client = FaucetClient(FAUCET_URL, rest_client)  # <:!:section_1

#     #:!:>section_2
#     alice = Account.generate()
#     bob = Account.generate()  # <:!:section_2

#     collection_name = "Alice's"
#     token_name = "Alice's first token"
#     property_version = 0

#     print("\n=== Addresses ===")
#     print(f"Alice: {alice.address()}")
#     print(f"Bob: {bob.address()}")

#     #:!:>section_3
#     faucet_client.fund_account(alice.address(), 100_000_000)
#     faucet_client.fund_account(bob.address(), 100_000_000)  # <:!:section_3

#     print("\n=== Initial Coin Balances ===")
#     print(f"Alice: {rest_client.account_balance(alice.address())}")
#     print(f"Bob: {rest_client.account_balance(bob.address())}")

#     print("\n=== Creating Collection and Token ===")

#     #:!:>section_4
#     txn_hash = rest_client.create_collection(
#         alice, collection_name, "Alice's simple collection", "https://aptos.dev"
#     )  # <:!:section_4
#     rest_client.wait_for_transaction(txn_hash)

#     #:!:>section_5
#     # see in:
#     # > https://github.com/aptos-labs/aptos-core/blob/main/aptos-move/framework/aptos-token/sources/token.move
#     txn_hash = rest_client.create_token(
#         alice,
#         collection_name,
#         token_name,
#         "Alice's simple token",
#         1,
#         "https://aptos.dev/img/nyan.jpeg",
#         0,
#     )  # <:!:section_5
#     rest_client.wait_for_transaction(txn_hash)

#     txn_hash = rest_client.create_token(
#     alice,
#     collection_name,
#     "Alice's second token",
#     "Alice's simple token*2",
#     1,
#     "https://baidu.com",
#     0,
# )  # <:!:section_5
#     rest_client.wait_for_transaction(txn_hash)

#     #:!:>section_6
#     collection_data = rest_client.get_collection(alice.address(), collection_name)
#     print(
#         f"Alice's collection: {json.dumps(collection_data, indent=4, sort_keys=True)}"
#     )  # <:!:section_6
#     #:!:>section_7
#     balance = rest_client.get_token_balance(
#         alice.address(), alice.address(), collection_name, token_name, property_version
#     )
#     print(f"Alice's token balance: {balance}")  # <:!:section_7
#     #:!:>section_8
#     token_data = rest_client.get_token_data(
#         alice.address(), collection_name, token_name, property_version
#     )
#     print(
#         f"Alice's token data: {json.dumps(token_data, indent=4, sort_keys=True)}"
#     )  # <:!:section_8

#     print("\n=== Transferring the token to Bob ===")
#     #:!:>section_9
#     txn_hash = rest_client.offer_token(
#         alice,
#         bob.address(),
#         alice.address(),
#         collection_name,
#         token_name,
#         property_version,
#         1,
#     )  # <:!:section_9
#     rest_client.wait_for_transaction(txn_hash)

#     #:!:>section_10
#     txn_hash = rest_client.claim_token(
#         bob,
#         alice.address(),
#         alice.address(),
#         collection_name,
#         token_name,
#         property_version,
#     )  # <:!:section_10
#     rest_client.wait_for_transaction(txn_hash)

#     balance = rest_client.get_token_balance(
#         alice.address(), alice.address(), collection_name, token_name, property_version
#     )
#     print(f"Alice's token balance: {balance}")
#     balance = rest_client.get_token_balance(
#         bob.address(), alice.address(), collection_name, token_name, property_version
#     )
#     print(f"Bob's token balance: {balance}")

#     print("\n=== Transferring the token back to Alice using MultiAgent ===")
#     #:!:>section_11
#     txn_hash = rest_client.direct_transfer_token(
#         bob, alice, alice.address(), collection_name, token_name, 0, 1
#     )  # <:!:section_11
#     rest_client.wait_for_transaction(txn_hash)

#     balance = rest_client.get_token_balance(
#         alice.address(), alice.address(), collection_name, token_name, property_version
#     )
#     print(f"Alice's token balance: {balance}")
#     balance = rest_client.get_token_balance(
#         bob.address(), alice.address(), collection_name, token_name, property_version
#     )
#     print(f"Bob's token balance: {balance}")

#     rest_client.close()
