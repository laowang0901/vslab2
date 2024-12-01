# Task ventilator
# Binds PUSH socket to tcp://localhost:50011
# Sends sentence to workers via that socket


import pickle
import zmq
import time

import constPipe

import nltk

context = zmq.Context()

# Socket to send workload on
sender = context.socket(zmq.PUSH)
address = "tcp://" + constPipe.SRC1 + ":" + constPipe.PORT1
sender.bind(address)

# Use NLTK(Natural Language Toolkit) to split text into sentences(pipenv install nltk)
f = open("../testText.txt", "r") 
text = f.read()
nltk.download('punkt_tab')
sentences = nltk.sent_tokenize(text)

print("Press Enter when the workers are ready: ")
_ = input()

print("Sending tasks to workers...")

time.sleep(1) # wait to allow all clients to connect

count = 0
for sentence in sentences: 
    count += 1
    sender.send(pickle.dumps((sentence)))  # send workload to worker
    print("{}. sentence: {}".format(count, sentence))
