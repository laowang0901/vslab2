# Task sink
# Binds PULL socket to tcp://localhost:50012 or tcp://localhost:50013
# Collects words from workers via that socket
# count words and print out result

import pickle
import sys
import time
import zmq

import constPipe
from collections import Counter


me = str(sys.argv[1])
context = zmq.Context()

# Socket to receive messages on
receiver = context.socket(zmq.PULL)
src = constPipe.SRC2 if me == '1' else constPipe.SRC3  # set task src host
prt = constPipe.PORT2 if me == '1' else constPipe.PORT3  # set task src port

address = "tcp://" + src + ":" + prt  # how and where to connect
receiver.bind(address)


time.sleep(1) 

print("Reducer {} started".format(me))

counter = {}

while True:
    work = pickle.loads(receiver.recv())  # receive work from a source
    if "STOP" not in work:
        if work[1] in counter:
            count = counter.get(work[1])
            counter.update({work[1]: count+1})
        else:
            counter[work[1]] = 1
        print("{} received workload from {}:  ({}: {})"
                .format(me, work[0], work[1], counter[work[1]]))

    else:
        break

print("All word collected:")
for key, value in counter.items():
    print("({}: {})".format(key, value))

