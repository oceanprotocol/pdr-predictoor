First cut: it may work, with errors

## Flow
- reads from subgraph list of template3 contracts, this gets list of all template3 deployed contracts
- for every contract, monitors when epoch is changing
- once we can predict a value, we call predict_function in prd_predictoors/predictions/predict.py. See below


## How to run

For full flow see [README](https://github.com/oceanprotocol/pdr-trueval/blob/main/README_local_full_flow.md)

```bash
export RPC_URL=http://127.0.0.1:8545
export SUBGRAPH_URL="http://172.15.0.15:8000/subgraphs/name/oceanprotocol/ocean-subgraph"
export PRIVATE_KEY="xxx"
export STAKE_AMOUNT=1
export CONTRACTS_TO_PREDICT="[]"
export STAKE_TOKENS="[]"
```
where:
  - STAKE_AMOUNT  = maximum stake (in decimal) for each prediction.  See predicted_confidence below
  - CONTRACTS_TO_PREDICT = if not present or empty, it will predict on all existing template3 contracts deployed on the network.  There can be a lot :) Narrow the scope with contract addresses
  - STAKE_TOKEN = combined with above, narrow scope only to template3 contracts that are using a specific list of STAKE_TOKENS (ie: Ocean). If not present or empty, will predict and stake everywhere :)

Install requirements if needed
```bash
pip install -r requirements.txt 
```

Start the predictoor:
```bash
python3 main.py
```

## Fork and customize
  The actual prediction code is in [prd_predictoors/predictions/predict.py](https://github.com/oceanprotocol/pdr-predictoors/blob/main/pdr_predictoors/predictions/predict.py#L3-L8).
  
  We call predict_function with 2 args:
   - topic:  this is ERC20.name
   - estimated_time:  estimated timestamp of block that we are going to predict.   This is informal, blockchain mining time is not accurate
  
  Function returns two variables:
   - predicted_value:  boolean, up/down
   - predicted_confidence:   int, 1 -> 100%. This sets the stake (STAKE_AMOUNT * predicted_confidence/100) that you are willing to put in your prediction.


  You need to change the function code and do some of your stuff. Now, it's just doing some random predictions

## TO DO
  - [ ]  - implement logic for STAKE_TOKENS and CONTRACTS_TO_PREDICT
  - [ ]  - improve payouts collect flow
  - [ ]  - check for balances 
  - [ ]  - improve approve/allowence flow