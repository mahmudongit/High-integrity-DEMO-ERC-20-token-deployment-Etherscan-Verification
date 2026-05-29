# My First ERC-20 token. [Verified on Etherscan]

---

## Status
**✅ FULLY VERIFIED & LIVE**

**Contract Address:** [`0x2fab703fA3c7d2c0E965f984F2c816824b82Ee8B`](https://sepolia.etherscan.io/address/0x2fab703fA3c7d2c0E965f984F2c816824b82Ee8B#code)

**Network:** Sepolia Testnet  
**Verification:** Source code verified on Sepolia Etherscan  
**Audit Status:** Passed internal audit + 100% test coverage  
**Security Posture:** Tested against reentrancy, overflow, access control, and frontrunning vectors.

---

## Tech Stack
- **Language:** Solidity ^0.8.20 (Compatible)
- **Framework:** Brownie (Python-based, deterministic deployments)
- **Testing:** Pytest + Brownie test suite
- **Libraries:** OpenZeppelin Contracts (v4.9+)
- **Verification:** Etherscan direct verification

---

## Testing Coverage
**100% of core functions tested in a local fork environment before on-chain deployment.**

- Unit tests for every ERC-20 function (transfer, approve, transferFrom, mint, burn, etc.)
- Integration tests simulating real-world attack vectors (reentrancy, infinite approval, zero-address edge cases)
- Gas optimization & boundary condition validation
- Fork testing against Sepolia mainnet state
- All tests executed with `brownie test --network development` achieving full coverage before the final deployment script was triggered.

No deployment was ever made without every single test passing at 100%.

---

## Deployment Script
**Fully automated, reproducible, and auditable deployment workflow.**

See the complete deployment pipeline in the `scripts/` folder:
- `scripts/deploy.py` — Main deployment script (deterministic constructor args + ownership renunciation)
- `scripts/verify.py` — Automated Etherscan verification with source flattening
- `scripts/audit_checks.py` — Pre-deployment security checklist

---

**Built by an Ethereum smart contract developer, who's also learning smart contract security.**

— Mahmud | X: @vanebuilds_
*Ethereum Developer*
