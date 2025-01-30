from brownie import network, config, accounts, MockV3Aggregator
from web3 import Web3
from brownie.network.gas.strategies import LinearScalingStrategy

DECIMALS = 8
STARTING_PRICE = 200000000000
LOCAL_BLOCKCHAIN_ENVIROMENTS = ["development", "ganache-local"]
# Configuración del precio de gas
gas_strategy = LinearScalingStrategy("60 gwei", "70 gwei", 1.1)

def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])
    
def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    MockV3Aggregator.deploy(
        DECIMALS, STARTING_PRICE, 
        {"from": get_account(), "gas_price": gas_strategy}
    )
    price_feed_address = MockV3Aggregator[-1].address
    print("Mocks deployed")