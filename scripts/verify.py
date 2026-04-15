from brownie import YourToken, network
from web3 import Web3

def main(address=None):
    if not address:
        print("Usage: brownie run scripts/verify.py main <address> --network sepolia")
        return

    if not Web3.is_address(address):
        print(f"Invalid address: {address}")
        return

    try:
        # Load the contract object from the address
        print(f"Attempting to verify {address} on {network.show_active()}...")
        contract_to_verify = YourToken.at(address)
        
        # Pass the OBJECT, not the string
        YourToken.publish_source(contract_to_verify)
        
        print("✅ Verification successful!")
    except Exception as e:
        print(f"❌ Verification failed: {e}")
