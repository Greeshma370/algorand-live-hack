Algorand ASA with Role Management (Manager, Reserve, Freeze, Clawback)
This Python script demonstrates advanced features of Algorand Standard Assets (ASA) using the algokit-utils library and LocalNet setup.

Features:
Creates a new ASA named RoleToken with all four roles set:

Manager

Reserve

Freeze

Clawback

Random test accounts are created and funded via the LocalNet dispenser.

A test user opts in to the asset and receives tokens.

The Freeze role freezes the test user’s asset holding.

The Clawback role revokes (claws back) 5 tokens from the test user to the clawback account.

Balance and freeze status are printed for verification.

This script is ideal for learning how ASA role permissions are enforced on Algorand. Requires LocalNet running and Python environment with algokit-utils.


