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

nltk.download('punkt_tab')


me = str(sys.argv[1])
context = zmq.Context()

# Socket to receive messages on
receiver = context.socket(zmq.PULL)
address = "tcp://" + constPipe.SRC1 + ":" + constPipe.PORT1
receiver.connect(address)

# Socket to send messages to
sender = context.socket(zmq.PUSH)
address1 = "tcp://" + constPipe.SRC2 + ":" + constPipe.PORT2
address2 = "tcp://" + constPipe.SRC3 + ":" + constPipe.PORT3
sender.connect(address1)
sender.connect(address2)

time.sleep(1) 

print("Mapper {} started".format(me))
count = 0

while True:
    count += 1
    sentence = pickle.loads(receiver.recv())  # receive work from a source
    print("{} received {}. workload: {}".format(me, count, sentence))
    words = nltk.word_tokenize(sentence)

    # Send results to sink
    for word in words:
        sender.send(pickle.dumps((me, word)))
        print("{} send workload {}".format(me, word))
        time.sleep(0.1)