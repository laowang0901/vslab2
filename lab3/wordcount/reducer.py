# Task sink
# Binds PULL socket to tcp://localhost:50012 or tcp://localhost:50013
# Collects words from workers via that socket
# count words and print out result

import pickle
import sys
import time
import zmq

import constPipe


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
count = 0

while True:
    count += 1
    work = pickle.loads(receiver.recv())  # receive work from a source
    print("{} received {}. workload {} from {}".format(me,count, work[1], work[0]))
    time.sleep(work[1] * 0.01)  # pretend to work