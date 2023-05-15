
import json
import os
from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import Web3, HTTPProvider, WebsocketProvider
from web3.middleware import construct_sign_and_send_raw_middleware

private_key = os.environ.get("PRIVATE_KEY")
assert private_key is not None, "You must set PRIVATE_KEY environment variable"
assert private_key.startswith("0x"), "Private key must start with 0x hex prefix"

# instantiate Web3 instance
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
private_key = os.environ.get("PRIVATE_KEY")
account: LocalAccount = Account.from_key(private_key)
w3.middleware_onion.add(construct_sign_and_send_raw_middleware(account))


class Token:
    def __init__(self, address):
        self.contract_address = address
        """ Temporary solution until we have ocean-contracts published in pypi"""
        with open('~/.ocean/ocean-contracts/artifacts/contracts/templates/ERC20Template3.sol/ERC20Template3.json') as f:
            data = json.load(f)
            abi = data['abi']
        self.contract_instance = w3.eth.contract(address=address, abi=abi)

    def allowance(self,account,spender):
        return self.contract_instance.allowance(account,spender).call()

    def balanceOf(self,account):
        return self.contract_instance.balanceOf(account).call()
    
    def approve(self,account,spender,amount):
        return self.contract_instance.approve(spender,amount).transact({"from":account})


class PredictorContract:
    def __init__(self, address):
        self.contract_instance = w3.eth.contract(address=address, abi=abi)
    
    def soonest_block_to_predict(self,block):
        return self.contract_instance.soonestBlockToPredict(block).call()
    def get_current_epoch(self):
        return self.contract_instance.curEpoch().call()
    
    def submit_prediction(self,predicted_value,stake_amount,prediction_block):
        """ Sumbits a prediction"""
        stake_token = Token(self.contract_instance.stakeToken().call())
        # TO DO - check allowence
        stake_token.approve(self.owner,self.contract_address,w3.to_wei(str(stake_amount)))
        self.contract_instance.submitPredval(predicted_value,w3.to_wei(str(stake_amount)),prediction_block)



