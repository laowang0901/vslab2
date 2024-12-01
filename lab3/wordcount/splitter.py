# Task ventilator
# Binds PUSH socket to tcp://localhost:50011
# Sends batch of tasks to workers via that socket
#

import pickle
import zmq
import random
import time

import constPipe

context = zmq.Context()

# Socket to send messages on
sender = context.socket(zmq.PUSH)
address = "tcp://" + constPipe.SRC1 + ":" + constPipe.PORT1
sender.bind(address)

print("Press Enter when the workers are ready: ")
_ = input()
print("Sending tasks to workers...")

time.sleep(1) # wait to allow all clients to connect

for i in range(100):  # generate 100 workloads
    workload = random.randint(1, 100)  # compute workload
    sender.send(pickle.dumps((workload)))  # send workload to worker
    print("Sending {}. tasks".format(i))
