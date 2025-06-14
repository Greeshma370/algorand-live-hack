SmartASAController – Algorand ARC-4 Whitelist Minting Contract
This ARC-4 compliant smart contract (SmartASAController) allows controlled creation, minting, and transfer of Algorand Standard Assets (ASA) with a built-in whitelist mechanism.

Features
Asset Creation: Only the app creator can create a new ASA.

Whitelist Management:

Add/remove accounts from a whitelist per ASA ID.

Only whitelisted addresses can receive minted tokens.

Minting:

Creator can mint ASA tokens to whitelisted addresses only.

Transfers:

Only allowed if the receiver is whitelisted.

Technology Stack
algopy for smart contract logic.

ARC-4 ABI methods to enable frontend integrations.

Use Case
Ideal for token-gated access, credential distribution, loyalty programs, or any system requiring permissioned minting and transfer.

To deploy this contract, use AlgoKit or Algorand’s testing environment with algopy and ARC-4 support.
