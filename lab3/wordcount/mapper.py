# Task worker
# Connects PULL socket to tcp://localhost:50011
# Collects sentence from ventilator via that socket
# Connects PUSH socket to tcp://localhost:50012 and tcp://localhost:50013
# Sends words to sink via that socket

import pickle
import sys
import time
import zmq

import constPipe

import nltk
import re

def remove_punctuation(sentence):
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

    for ele in sentence:
        if ele in punc:
            sentence = sentence.replace(ele, "")
    
    return sentence


nltk.download('punkt_tab')

me = str(sys.argv[1])
context = zmq.Context()

# Socket to receive messages on
receiver = context.socket(zmq.PULL)
address = "tcp://" + constPipe.SRC1 + ":" + constPipe.PORT1
receiver.connect(address)

# Socket to send messages to
sender1 = context.socket(zmq.PUSH)
sender2 = context.socket(zmq.PUSH)
address1 = "tcp://" + constPipe.SRC2 + ":" + constPipe.PORT2
address2 = "tcp://" + constPipe.SRC3 + ":" + constPipe.PORT3
sender1.connect(address1)
sender2.connect(address2)

time.sleep(1) 

print("Mapper {} started".format(me))
count = 0

while True:
    count += 1
    sentence = pickle.loads(receiver.recv())  # receive work from a source
    if "STOP" not in sentence:
        print("{} received {}. workload: {}".format(me, count, sentence))
        sentence = remove_punctuation(sentence)
        words = nltk.word_tokenize(sentence)

        # Send results to sink
        for word in words:
            word = word.lower()
            if re.match(r'[a-o]', word):
                sender1.send(pickle.dumps((me, word)))
            else:
                sender2.send(pickle.dumps((me, word)))
            print("{} send workload {}".format(me, word))
            time.sleep(0.1)
            
    else:
        sender1.send(pickle.dumps((me, "STOP")))
        sender2.send(pickle.dumps((me, "STOP")))
        