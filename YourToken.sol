// SPDX-License-Identifier: MIT
pragma solidity 0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Pausable.sol";
import "@openzeppelin/contracts/access/Ownable2Step.sol";

/// @title YourToken - A secure ERC-20 token with pausable and burnable features
/// @notice This contract implements a standard ERC-20 token with additional security features
/// @dev Inherits from OpenZeppelin v5.x contracts for maximum security and audit readiness
contract YourToken is ERC20, ERC20Burnable, ERC20Pausable, Ownable2Step {
    error ZeroAddressOwner();
    error ZeroAddressRecipient();
    error ZeroAmount();
    error CapExceeded(uint256 attemptedSupply, uint256 maxSupply);

    uint8 private constant DECIMALS = 18;
    uint256 public immutable maxSupply;

    /// @notice Constructor to initialize the token
    /// @param tokenName The name of the token
    /// @param tokenSymbol The symbol of the token
    /// @param initialSupply The initial supply of tokens (without decimals)
    /// @param supplyCap The maximum supply of tokens (without decimals)
    constructor(
        string memory tokenName,
        string memory tokenSymbol,
        uint256 initialSupply,
        uint256 supplyCap
    ) ERC20(tokenName, tokenSymbol) Ownable(msg.sender) {
        uint256 scaledCap = supplyCap * 10 ** DECIMALS;
        uint256 scaledInitialSupply = initialSupply * 10 ** DECIMALS;

        if (scaledCap == 0) revert ZeroAmount();
        if (scaledInitialSupply == 0) revert ZeroAmount();
        if (scaledInitialSupply > scaledCap) {
            revert CapExceeded(scaledInitialSupply, scaledCap);
        }

        maxSupply = scaledCap;

        // Mint initial supply to the deployer
        _mint(msg.sender, scaledInitialSupply);
    }

    /// @notice Returns the number of decimals used for token display
    /// @return The number of decimals (18)
    function decimals() public pure override returns (uint8) {
        return DECIMALS;
    }

    /// @notice Mint new tokens (owner only)
    /// @dev Only the owner can mint new tokens up to the immutable supply cap
    /// @param to The address to receive the minted tokens
    /// @param amount The amount of tokens to mint (without decimals)
    function mint(address to, uint256 amount) public onlyOwner {
        if (to == address(0)) revert ZeroAddressRecipient();
        if (amount == 0) revert ZeroAmount();

        uint256 scaledAmount = amount * 10 ** DECIMALS;
        uint256 newSupply = totalSupply() + scaledAmount;
        if (newSupply > maxSupply) revert CapExceeded(newSupply, maxSupply);

        _mint(to, scaledAmount);
    }

    /// @notice Transfers ownership to a new address using the two-step flow
    /// @dev Adds explicit zero-address validation to silence static-analysis warnings
    /// @param newOwner The address proposed as the next owner
    function transferOwnership(address newOwner) public override onlyOwner {
        if (newOwner == address(0)) revert ZeroAddressOwner();
        super.transferOwnership(newOwner);
    }

    /// @notice Pause the contract (owner only)
    /// @dev Only the owner can pause the contract in case of emergency
    function pause() public onlyOwner {
        _pause();
    }

    /// @notice Unpause the contract (owner only)
    /// @dev Only the owner can unpause the contract
    function unpause() public onlyOwner {
        _unpause();
    }

    /// @notice Internal function to update token balances
    /// @dev Overrides required for ERC20Pausable compatibility
    /// @param from The sender address
    /// @param to The receiver address
    /// @param value The amount of tokens to transfer
    function _update(
        address from,
        address to,
        uint256 value
    ) internal override(ERC20, ERC20Pausable) {
        super._update(from, to, value);
    }
}
