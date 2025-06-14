from algokit_utils import Account
from algokit_utils.algorand import AlgorandClient
from algokit_utils.models.amount import AlgoAmount
from algokit_utils.transactions.transaction_composer import (
    AssetCreateParams,
    AssetOptInParams,
    AssetTransferParams,
    AssetFreezeParams,
)

# Set up Algorand client (LocalNet for testing)
algorand = AlgorandClient.default_localnet()

# Create/fund accounts for roles and a test user
manager = algorand.account.random()
reserve = algorand.account.random()
freeze = algorand.account.random()
clawback = algorand.account.random()
test_user = algorand.account.random()
dispenser = algorand.account.localnet_dispenser()
for acct in [manager, reserve, freeze, clawback, test_user]:
    algorand.account.ensure_funded(acct, dispenser, min_spending_balance=AlgoAmount.from_algo(1))

# Create ASA with all roles set
asset_params = AssetCreateParams(
    sender=manager.address,
    total=1000,
    decimals=0,
    asset_name="RoleToken",
    unit_name="ROLE",
    manager=manager.address,
    reserve=reserve.address,
    freeze=freeze.address,
    clawback=clawback.address,
)
result = algorand.send.asset_create(asset_params)
asset_id = int(result.confirmation["asset-index"])
print("ASA created with Asset ID:", asset_id)

# Opt-in test user
algorand.send.asset_opt_in(
    AssetOptInParams(
        sender=test_user.address,
        asset_id=asset_id,
        signer=test_user.signer
    )
)

# Opt-in the clawback address to the asset before receiving tokens via clawback
algorand.send.asset_opt_in(
    AssetOptInParams(
        sender=clawback.address,
        asset_id=asset_id,
        signer=clawback.signer
    )
)

# Transfer some tokens to test user
algorand.send.asset_transfer(
    AssetTransferParams(
        sender=manager.address,
        receiver=test_user.address,
        asset_id=asset_id,
        amount=10
    )
)

# Demonstrate freeze
algorand.send.asset_freeze(
    AssetFreezeParams(
        sender=freeze.address,
        asset_id=asset_id,
        account=test_user.address,
        frozen=True
    )
)
print(f"Account {test_user.address} frozen for asset {asset_id}")

# Demonstrate clawback (revoke 5 tokens from test_user to clawback address)
algorand.send.asset_transfer(
    AssetTransferParams(
        sender=clawback.address,           # Must be the clawback address
        receiver=clawback.address,         # Where the clawed-back tokens will go
        asset_id=asset_id,
        amount=5,
        clawback_target=test_user.address  # The account to revoke from
    )
)
print(f"Clawed back 5 units from {test_user.address}")

# Check test user balance and frozen status
info = algorand.asset.get_account_information(test_user, asset_id)
print(f"Test user balance: {info.balance}, frozen: {info.frozen}")