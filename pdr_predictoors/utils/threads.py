import time
import os

from threading import Thread
from pdr_predictoors.predictions.predict import predict_function

class NewPrediction(Thread):
    def __init__(self,topic,predictor_contract,current_block_num,avergage_time_between_blocks):
        # execute the base constructor
        Thread.__init__(self)
        # set a default value
        self.values = { "last_submited_epoch": topic["last_submited_epoch"],
                      "contract_address": topic["last_submited_epoch"]
                      }
        self.topic = topic
        self.predictor_contract = predictor_contract
        self.current_block_num = current_block_num
        self.avergage_time_between_blocks = avergage_time_between_blocks

    def run(self):
        """ Add 5 blocks, because it will take some time to 1) calculate a prediction 2) submit tx  3) wait for tx to confirm"""
        soonest_block = self.predictor_contract.soonest_block_to_predict(self.current_block_num+5)
        estimated_time = time.now() + (soonest_block - self.current_block_num)* self.avergage_time_between_blocks
        (predicted_value,predicted_confidence) = predict_function(self.topic['name'],estimated_time)
        """ We have a prediction, let's submit it"""
        stake_amount = os.getenv("stakeAmount",1)*predicted_confidence/100
        self.predictor_contract.submit_prediction(predicted_value,stake_amount,soonest_block)
