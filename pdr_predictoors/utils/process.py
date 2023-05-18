import threading
from pdr_predictoors.utils.subgraph import get_all_interesting_prediction_contracts
from pdr_predictoors.utils.contract import PredictorContract
from pdr_predictoors.utils.threads import NewPrediction

""" Get all intresting topics that we can predict.  Like ETH-USDT, BTC-USDT """
topics = get_all_interesting_prediction_contracts()
def process_block(block,avergage_time_between_blocks):
    global topics
    """ Process each contract and see if we need to submit """
    print(f"Got new block: {block['number']}...")
    if not topics:
        topics = get_all_interesting_prediction_contracts()
    threads=[]
    for address in topics:
        topic = topics[address]
        predictor_contract = PredictorContract(address)
        epoch = predictor_contract.get_current_epoch()
        if epoch > topic['last_submited_epoch']:
            """ Let's make a prediction & claim rewards"""
            thr = NewPrediction(topic,predictor_contract,block["number"],avergage_time_between_blocks,epoch)
            thr.start()
            threads.append(thr)
    """ Wait for all threads to finish"""
    for thr in threads:
        thr.join()
        address=thr.values['contract_address'].lower()
        new_epoch = thr.values['last_submited_epoch']
        topics[address]["last_submited_epoch"]=new_epoch
        


