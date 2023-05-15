
import json
import os
from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import Web3, HTTPProvider, WebsocketProvider
from web3.middleware import construct_sign_and_send_raw_middleware
from os.path import expanduser
home = expanduser("~")

private_key = os.environ.get("PRIVATE_KEY")
assert private_key is not None, "You must set PRIVATE_KEY environment variable"
assert private_key.startswith("0x"), "Private key must start with 0x hex prefix"

# instantiate Web3 instance
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
private_key = os.environ.get("PRIVATE_KEY")
account: LocalAccount = Account.from_key(private_key)
owner = account.address
w3.middleware_onion.add(construct_sign_and_send_raw_middleware(account))


""" Temporary solution until we have ocean-contracts published in pypi"""
f = open(home+'/.ocean/ocean-contracts/artifacts/contracts/templates/ERC20Template3.sol/ERC20Template3.json')
data=json.load(f)
abi = data['abi']


class Token:
    def __init__(self, address):
        self.contract_address = w3.to_checksum_address(address)
        self.contract_instance = w3.eth.contract(address=w3.to_checksum_address(address), abi=abi)

    def allowance(self,account,spender):
        return self.contract_instance.functions.allowance(account,spender).call()

    def balanceOf(self,account):
        return self.contract_instance.functions.balanceOf(account).call()
    
    def approve(self,spender,amount):
        gasPrice = w3.eth.gas_price
        #print(f"Approving {amount} for {spender} on contract {self.contract_address}")
        try:
            tx = self.contract_instance.functions.approve(spender,amount).transact({"from":owner,"gasPrice":gasPrice})
            receipt = w3.eth.wait_for_transaction_receipt(tx)
            return receipt
        except:
            return None


class PredictorContract:
    def __init__(self, address):
        self.contract_address = w3.to_checksum_address(address)
        self.contract_instance = w3.eth.contract(address=w3.to_checksum_address(address), abi=abi)
    
    def soonest_block_to_predict(self,block):
        return self.contract_instance.functions.soonestBlockToPredict(block).call()
    def get_current_epoch(self):
        return self.contract_instance.functions.curEpoch().call()
    
    def submit_prediction(self,predicted_value,stake_amount,prediction_block):
        """ Sumbits a prediction"""
        stake_token = Token(self.contract_instance.functions.stakeToken().call())
        # TO DO - check allowence
        amount_wei = w3.to_wei(str(stake_amount),'ether')
        stake_token.approve(self.contract_address,amount_wei)
        gasPrice = w3.eth.gas_price
        try:
            tx = self.contract_instance.functions.submitPredval(predicted_value,amount_wei,prediction_block).transact({"from":owner,"gasPrice":gasPrice})
            receipt = w3.eth.wait_for_transaction_receipt(tx)
            return receipt
        except:
            return None
    
    def get_trueValSubmitTimeoutBlock(self):
        return self.contract_instance.functions.trueValSubmitTimeoutBlock().call()
    
    def get_blocksPerEpoch(self):
        return self.contract_instance.functions.blocksPerEpoch().call()
    
    def get_prediction(self,slot):
        return self.contract_instance.functions.getPrediction(slot).call({"from":owner})
    
    def payout(self,slot):
        """ Claims the payout for a slot"""
        gasPrice = w3.eth.gas_price
        try:
            tx = self.contract_instance.functions.payout(slot,owner).transact({"from":owner,"gasPrice":gasPrice})
            receipt = w3.eth.wait_for_transaction_receipt(tx)
            return receipt
        except:
            return None



