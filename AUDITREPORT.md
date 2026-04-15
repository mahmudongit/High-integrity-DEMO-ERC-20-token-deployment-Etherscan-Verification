brownie run scripts/audit_checks.py main "0x2fab703fA3c7d2c0E965f984F2c816824b82Ee8B" --network sepolia
 sepolia
Brownie v1.21.0 - Python development framework for Ethereum

PowProject is the active project.

Running 'scripts\audit_checks.py::main'...
--- 🛡️  HIGH-INTEGRITY AUDIT REPORT for: 0x2fab703fA3c7d2c0E965f984F2c816824b82Ee8B ---
Network: sepolia
============================================================

[1] 📋 Metadata Check:
    Name     : erc20demotoken
    Symbol   : EDT
    Decimals : 18

[2] 📊 Supply Check:
    Total Supply : 1,000,000 EDT

[3] 🔐 Security Check - Ownership:
    Current Owner : 0x1157fEa8690C2BA2a23fb33Fa650c665527e7F53
    ℹ️  Owner is an external wallet (recommended)

[4] 💰 Deployer Balance Check:
    Deployer      : 0x1157fEa8690C2BA2a23fb33Fa650c665527e7F53
    Balance       : 1,000,000 EDT
    ✅ Deployer holds 100% of the initial supply (standard for fair launch)

============================================================
✅ Audit Script Completed Successfully – Contract looks clean
Proceed to full manual audit + formal verification if going to mainnet.
