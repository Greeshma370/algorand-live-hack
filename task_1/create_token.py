from algokit_utils import Account, SigningAccount
from algokit_utils.algorand import AlgorandClient
from algokit_utils.models.amount import AlgoAmount
from algokit_utils.transactions.transaction_composer import (
    AssetCreateParams,
    AssetOptInParams,
    AssetTransferParams,
)

# 1. Set up Algorand client (using LocalNet for testing)
algorand = AlgorandClient.default_localnet()

# 2. Create/fund sender and receiver accounts
sender = algorand.account.random()
receiver = algorand.account.random()
dispenser = algorand.account.localnet_dispenser()
algorand.account.ensure_funded(sender, dispenser, min_spending_balance=AlgoAmount.from_algo(10))
algorand.account.ensure_funded(receiver, dispenser, min_spending_balance=AlgoAmount.from_algo(1))

# 3. Create the ASA (token)
asset_params = AssetCreateParams(
    sender=sender.address,
    total=1_000_000,           # Total supply
    decimals=2,                # Number of decimals
    asset_name="MyToken",      # Full name
    unit_name="MTK",           # Unit/ticker
    manager=sender.address,    # Set manager, reserve, freeze, clawback to sender
    reserve=sender.address,
    freeze=sender.address,
    clawback=sender.address,
)
create_result = algorand.send.asset_create(asset_params)
asset_id = int(create_result.confirmation["asset-index"])
print("ASA created with Asset ID:", asset_id)

# 4. Opt-in the receiver to the ASA
algorand.send.asset_opt_in(
    AssetOptInParams(
        sender=receiver.address,
        asset_id=asset_id,
        signer=receiver.signer
    )
)

# 5. Transfer tokens from sender to receiver
transfer_amount = 100  # Amount to transfer (in base units, considering decimals)
transfer_result = algorand.send.asset_transfer(
    AssetTransferParams(
        sender=sender.address,
        receiver=receiver.address,
        asset_id=asset_id,
        amount=transfer_amount
    )
)
print("Transfer completed. TxID:", transfer_result.tx_id)

# 6. Verify the transfer
receiver_balance = algorand.asset.get_account_information(receiver, asset_id)
print("Receiver balance:", receiver_balance.balance)