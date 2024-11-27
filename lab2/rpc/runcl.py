import rpc
import logging
import time

from context import lab_logging
    
def msg_print(result):
    print("Recieve result from server: {}".format(result))



lab_logging.setup(stream_level=logging.INFO)

cl = rpc.Client()
cl.run()

base_list = rpc.DBList({'foo'})

cl.append('bar', base_list, msg_print)
for i in range(1, 10):
    print("Client is doing someting else" + "." * i)
    time.sleep(1.5)

cl.stop()