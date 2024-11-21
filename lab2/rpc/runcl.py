import rpc
import logging
import threading
import time

from context import lab_logging


lab_logging.setup(stream_level=logging.INFO)

cl = rpc.Client()
cl.run()

base_list = rpc.DBList({'foo'})

background = threading.Thread(target=cl.append, args=('bar', base_list, cl.callback_print))
background.start()
for i in range(1, 10):
    print("Client is doing someting else" + "." * i)
    time.sleep(1.5)
background.join()  # Wait for the background task to finish

cl.stop()