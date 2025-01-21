import constRPC
import threading
import time

from context import lab_channel


class DBList:
    def __init__(self, basic_list):
        self.value = list(basic_list)

    def append(self, data):
        self.value = self.value + [data]
        return self


class Client(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self) 
        self.chan = lab_channel.Channel()
        self.client = self.chan.join('client')
        self.server = None

    def run(self):
        self.chan.bind(self.client)
        self.server = self.chan.subgroup('server')


    def stop(self):
        self.chan.leave('client')
        
    def wait_for_response(self, callback):
        msgrcv = self.chan.receive_from(self.server)  # wait for response
        callback(msgrcv[1].value)
       
    
    def append(self, data, db_list, callback):
        assert isinstance(db_list, DBList)
        msglst = (constRPC.APPEND, data, db_list)  # message payload
        self.chan.send_to(self.server, msglst)  # send msg to server
        print("Request sent to the Server")
        msgrcv = self.chan.receive_from(self.server)  # wait for ack
        
        if constRPC.OK == msgrcv[1]:
            print("Server get request")
            background = threading.Thread(target=self.wait_for_response, args=(callback,))
            background.start()
    






class Server:
    def __init__(self):
        self.chan = lab_channel.Channel()
        self.server = self.chan.join('server')
        self.timeout = 3

    @staticmethod
    def append(data, db_list):
        assert isinstance(db_list, DBList)  # - Make sure we have a list
        return db_list.append(data)

    def run(self):
        self.chan.bind(self.server)
        while True:
            msgreq = self.chan.receive_from_any(self.timeout)  # wait for any request
            if msgreq is not None:
                client = msgreq[0]  # see who is the caller
                print("{} sent request".format(client))
                self.chan.send_to({client}, constRPC.OK)  # sending Acknowledgement back to cleint
                print("ACK sent to {}".format(client))
                msgrpc = msgreq[1]  # fetch call & parameters
                
                if constRPC.APPEND == msgrpc[0]:  # check what is being requested
                    time.sleep(10)  # waiting for 10 second
                    result = self.append(msgrpc[1], msgrpc[2])  # do local call
                    self.chan.send_to({client}, result)  # return response
                    print("Response sent to {}".format(client))

                else:
                    pass  # unsupported request, simply ignore
