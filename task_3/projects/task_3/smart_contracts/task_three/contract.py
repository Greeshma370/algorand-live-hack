from algopy import ARC4Contract, BoxMap, Txn, Global, urange, itxn, subroutine, UInt64, String, Account
from algopy.arc4 import abimethod, Address, DynamicArray

class SmartASAController(ARC4Contract):
    def __init__(self) -> None:
        # Map ASA ID to a list of whitelisted addresses
        self.whitelist = BoxMap(UInt64, DynamicArray[Address])
        self.asa_id = UInt64(0)
        self.total_minted = UInt64(0)

    @abimethod()
    def asset_create(
        self,
        total: UInt64,
        decimals: UInt64,
        unit_name: String,
        asset_name: String,
        url: String
    ) -> UInt64:
        assert Txn.sender == Global.creator_address, "Only creator can create ASA"

        itxn_result = itxn.AssetConfig(
            total=total,
            decimals=decimals,
            unit_name=unit_name,
            asset_name=asset_name,
            url=url,
            manager=Global.current_application_address,
            reserve=Global.current_application_address,
            freeze=Global.current_application_address,
            clawback=Global.current_application_address,
            fee=0
        ).submit()

        self.asa_id = itxn_result.created_asset.id
        return self.asa_id

    @abimethod()
    def add_to_whitelist(self, asa_id: UInt64, account: Address) -> None:
        assert Txn.sender == Global.creator_address, "Only creator can add to whitelist"

        if asa_id in self.whitelist:
            arr = self.whitelist[asa_id].copy()
            for idx in urange(arr.length):
                if arr[idx] == account:
                    return  # Already whitelisted
            arr.append(account)
            self.whitelist[asa_id] = arr.copy()
        else:
            new_arr = DynamicArray[Address]()
            new_arr.append(account)
            self.whitelist[asa_id] = new_arr.copy()

    @subroutine
    def is_whitelisted(self, asa_id: UInt64, account: Address) -> bool:
        if asa_id in self.whitelist:
            arr = self.whitelist[asa_id].copy()
            for idx in urange(arr.length):
                if arr[idx] == account:
                    return True
        return False

    @abimethod()
    def mint(self, asa_id: UInt64, amount: UInt64, receiver: Address) -> bool:
        assert Txn.sender == Global.creator_address, "Only creator can mint"
        assert self.is_whitelisted(asa_id, receiver), "Receiver not whitelisted"

        self.total_minted += amount

        itxn.AssetTransfer(
            xfer_asset=asa_id,
            asset_amount=amount,
            asset_sender=Global.current_application_address,
            asset_receiver=receiver.native,
            fee=0
        ).submit()
        return True

    @abimethod()
    def transfer(self, asa_id: UInt64, sender: Address, receiver: Address, amount: UInt64) -> bool:
        assert self.is_whitelisted(asa_id, receiver), "Receiver not whitelisted"

        itxn.AssetTransfer(
            xfer_asset=asa_id,
            asset_amount=amount,
            asset_sender=sender.native,
            asset_receiver=receiver.native,
            fee=0
        ).submit()
        return True

    @abimethod()
    def remove_from_whitelist(self, asa_id: UInt64, account: Address) -> None:
        assert Txn.sender == Global.creator_address, "Only creator can remove from whitelist"

        if asa_id in self.whitelist:
            arr = self.whitelist[asa_id].copy()
            new_arr = DynamicArray[Address]()
            for idx in urange(arr.length):
                if arr[idx] != account:
                    new_arr.append(arr[idx])
            self.whitelist[asa_id] = new_arr.copy()
