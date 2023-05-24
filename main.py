import time
import os

from pdr_predictoors.utils.process import process_block
from pdr_predictoors.utils.contract import w3


# TODO - check for all envs
assert os.environ.get("RPC_URL",None), "You must set RPC_URL environment variable"
assert os.environ.get("SUBGRAPH_URL",None), "You must set SUBGRAPH_URL environment variable"

avergage_time_between_blocks = 0
last_block_time=0

def log_loop(blockno):
    global avergage_time_between_blocks,last_block_time
    block = w3.eth.get_block(blockno, full_transactions=False)
    if block:
        if last_block_time>0:
            avergage_time_between_blocks = (avergage_time_between_blocks + (block["timestamp"] - last_block_time))/2
        last_block_time = block["timestamp"]
    process_block(block,avergage_time_between_blocks)
        

def main():
    print("Starting main loop...")
    lastblock =0
    while True:
        block = w3.eth.block_number
        if block>lastblock:
            lastblock = block
            log_loop(block)
        else:
            time.sleep(1)



if __name__ == '__main__':
    main()