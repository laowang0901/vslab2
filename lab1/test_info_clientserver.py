"""
Simple client server unit test
"""

import logging
import threading
import unittest

import info_clientserver
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)


class TestPhonebookService(unittest.TestCase):
    """The test"""
    phonebook = {'alice': '1234', 'bob': '5678'}
    _server = info_clientserver.Server()  # create single server in class variable
    _server_thread = threading.Thread(target=_server.serve(phonebook))  # define thread for running server


    @classmethod
    def setUpClass(cls):
        cls._server_thread.start()  # start server loop in a thread (called only once)

    def setUp(self):
        super().setUp()
        self.client = info_clientserver.Client()  # create new client for each test

    def test_srv_get(self): 
        """Test simple call"""
        msg = self.client.call("GET alice")
        self.assertEqual(msg, '1234')
    
    def test_srv_get2(self):
        """Test simple call"""
        msg = self.client.call("GET paul")
        self.assertEqual(msg, 'no matching data')
    
    def test_srv_get3(self):
        """Test simple call"""
        msg = self.client.call("Hello VS2Lab")
        self.assertEqual(msg, 'Invalid request')
    
    def test_srv_get4(self):
        """Test simple call"""
        msg = self.client.call("GET Hello VS2Lab")
        self.assertEqual(msg, 'no matching data')
    
    def test_srv_getAll(self):
        """Test simple call"""
        msg = self.client.call("GETALL")
        self.assertEqual(msg, 'alice : 1234\nbob : 5678\n')

    def tearDown(self):
        self.client.close()  # terminate client after each test

    @classmethod
    def tearDownClass(cls):
        cls._server._serving = False  # break out of server loop. pylint: disable=protected-access
        cls._server_thread.join()  # wait for server thread to terminate


if __name__ == '__main__':
    unittest.main()
