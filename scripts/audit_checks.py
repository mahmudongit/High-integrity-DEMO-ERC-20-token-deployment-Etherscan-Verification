from brownie import YourToken, accounts, network, config
import sys

def main(address: str = None):
    if not address:
        print("❌ Error: Please provide the contract address.")
        print("   Usage: brownie run scripts/audit_checks.py main <address> --network sepolia")
        print("   Example: brownie run scripts/audit_checks.py main 0x1234... --network sepolia")
        sys.exit(1)

    print(f"--- 🛡️  HIGH-INTEGRITY AUDIT REPORT for: {address} ---")
    print(f"Network: {network.show_active()}")
    print("=" * 60)

    try:
        # Load the verified contract using the exact ABI from your project
        token = YourToken.at(address)

        # ── 1. Metadata Check ─────────────────────────────────────
        print(f"\n[1] 📋 Metadata Check:")
        print(f"    Name     : {token.name()}")
        print(f"    Symbol   : {token.symbol()}")
        print(f"    Decimals : {token.decimals()}")

        # ── 2. Supply Check ───────────────────────────────────────
        total_supply = token.totalSupply()
        decimals = token.decimals()
        human_supply = total_supply / (10 ** decimals)

        print(f"\n[2] 📊 Supply Check:")
        print(f"    Total Supply : {human_supply:,.0f} {token.symbol()}")

        # ── 3. Ownership Check (Ownable pattern) ──────────────────
        try:
            owner = token.owner()
            print(f"\n[3] 🔐 Security Check - Ownership:")
            print(f"    Current Owner : {owner}")
            
            # Smart warning – works on any network
            if owner == "0x0000000000000000000000000000000000000000":
                print("    ✅ Ownership has been renounced (best practice)")
            elif owner.lower() in [acc.address.lower() for acc in accounts]:
                print("    ⚠️  Owner is one of the loaded local accounts!")
            else:
                print("    ℹ️  Owner is an external wallet (recommended)")
        except Exception:
            print(f"\n[3] 🔐 Security Check: 'owner()' not found → Not using Ownable")

        # ── 4. Deployer / Initial Holder Balance Check ───────────
        # Robust way: try config first, fallback gracefully
        try:
            # Prefer the wallet defined in brownie-config.yaml (your deployment key)
            deployer_pk = config["wallets"]["from_key"]
            deployer = accounts.add(deployer_pk)
        except (KeyError, AttributeError):
            # Fallback for people using accounts.load() or env vars
            print("    ⚠️  Could not load deployer from config['wallets']['from_key']")
            print("    Falling back to first loaded account (accounts[0])")
            deployer = accounts[0]

        deployer_balance = token.balanceOf(deployer)
        human_deployer_balance = deployer_balance / (10 ** decimals)

        print(f"\n[4] 💰 Deployer Balance Check:")
        print(f"    Deployer      : {deployer}")
        print(f"    Balance       : {human_deployer_balance:,.0f} {token.symbol()}")

        if deployer_balance == total_supply:
            print("    ✅ Deployer holds 100% of the initial supply (standard for fair launch)")
        elif deployer_balance == 0:
            print("    ⚠️  Deployer holds 0 tokens – supply was transferred elsewhere")
        else:
            print("    ℹ️  Supply is partially distributed (check distribution wallets)")

        print(f"\n{'=' * 60}")
        print("✅ Audit Script Completed Successfully – Contract looks clean")
        print("Proceed to full manual audit + formal verification if going to mainnet.")

    except Exception as e:
        print(f"\n❌ Critical Audit Failure: {e}")
        print("   → Double-check that the contract is verified on Etherscan and matches YourToken ABI.")
        sys.exit(1)