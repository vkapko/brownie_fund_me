from scripts.deploy import deploy_fund_me
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from brownie import accounts, network, exceptions
import pytest


def test_can_fund_and_withdraw():
    fund_me = deploy_fund_me()
    account = get_account()
    price = 0.01 * 10 ** 18
    print(f"Entrance fee: {price}")
    tx = fund_me.fund({"from": account, "value": price})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == price
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    account = get_account()
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
