from brownie import FundMe, MockV3Aggregator, Wei, config, network
from scripts.helpful_scripts import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIROMENTS
from web3 import Web3
from brownie.network.gas.strategies import LinearScalingStrategy

# Configuración del precio de gas
gas_strategy = LinearScalingStrategy("60 gwei", "70 gwei", 1.1)


def deploy_fund_me():
    account = get_account()
    
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    account = get_account()
    fund_me = FundMe.deploy(
    price_feed_address,
    {"from": account, "gas_price": gas_strategy},
    publish_source=config["networks"][network.show_active()].get("verify")
    )
    print(f"Deployed to {fund_me.address}")
    return fund_me

def main():
    deploy_fund_me()
