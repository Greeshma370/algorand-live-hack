This Python script demonstrates how to create and transfer an Algorand Standard Asset (ASA) using AlgoKit Utils. It works on a LocalNet setup and walks through the following steps:

Initializes a local Algorand client.

Creates two accounts: sender and receiver.

Funds both accounts using the LocalNet dispenser.

Creates an ASA (MyToken with 2 decimal places).

Opts in the receiver account to the ASA.

Transfers 100 tokens from sender to receiver.

Verifies and prints the receiver’s ASA balance.

This is ideal for testing ASA workflows and understanding basic token operations on Algorand. Make sure you have a LocalNet running and algokit-utils installed before executing.
