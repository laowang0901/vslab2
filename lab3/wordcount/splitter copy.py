import pickle
import sys
import time

import zmq

import constPipe

me = str(sys.argv[1])

src = constPipe.SRC
prt = constPipe.PORT1

context = zmq.Context()
push_socket = context.socket(zmq.PUSH)  # create a push socket

address = "tcp://" + src + ":" + prt  # how and where to connect
push_socket.bind(address)  # bind socket to address

time.sleep(1) # wait to allow all clients to connect

f = open("../testText.txt", "r")

print(f.read())
##TODO 
## split sentence into words with multiple separator 


##for i in range(100):  # generate 100 workloads
##    workload = random.randint(1, 100)  # compute workload
##    push_socket.send(pickle.dumps((me, workload)))  # send workload to worker
    
