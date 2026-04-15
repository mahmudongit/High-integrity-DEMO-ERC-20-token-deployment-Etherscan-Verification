from brownie import YourToken, accounts, network, config
from dotenv import load_dotenv
import os

load_dotenv()

SUPPORTED_NETWORKS = {"mainnet", "goerli", "sepolia", "polygon", "arbitrum"}

def main():
    active_network = network.show_active()
    if active_network not in SUPPORTED_NETWORKS:
        raise ValueError(f"Refusing to deploy to unsupported network: {active_network}")

    # Load account securely
    private_key = os.getenv('PRIVATE_KEY')
    if not private_key:
        raise ValueError("PRIVATE_KEY environment variable not set")
    account = accounts.add(private_key)

    # Constructor arguments (customize as needed)
    name = "erc20demotoken"
    symbol = "EDT"
    initial_supply = 1000000  # 1 million tokens
    supply_cap = 1000000      # hard cap: no inflation beyond initial allocation

    print(
        f"Deploying {name} ({symbol}) with initial supply {initial_supply} tokens "
        f"and supply cap {supply_cap} tokens on {active_network}..."
    )

    # Deploy with explicit EIP-1559 fee controls
    token = YourToken.deploy(
        name,
        symbol,
        initial_supply,
        supply_cap,
        {"from": account, "priority_fee": "2 gwei"}
    )

    # Wait for deployment confirmation
    print(f"Waiting for deployment confirmation...")
    token.tx.wait(3)  # Wait for 3 confirmations

    print(f"✅ Token successfully deployed!")
    print(f"📍 Contract Address: {token.address}")
    print(f"🔗 Transaction Hash: {token.tx.txid}")
    print(f"🌐 Network: {active_network}")

    # Automatic Etherscan verification
    if config["networks"][active_network].get("verify", False):
        print("🔍 Verifying contract on Etherscan...")
        try:
            YourToken.publish_source(token)
            print("✅ Verification successful!")
        except Exception as e:
            print(f"❌ Verification failed: {e}")
            print(f"Manual verification command: brownie run scripts/verify.py --address {token.address}")
    else:
        print("⚠️  Skipping verification (not configured for this network)")
        print(f"Manual verification command: brownie run scripts/verify.py --address {token.address}")

    return token
