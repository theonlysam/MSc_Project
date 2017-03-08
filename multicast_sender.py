'''
Name:  Marc Smith
Date:  2017-02-14
Description:
A multithreaded multicast server that listens for TCP connections from clients.
When the required number of clients connect multicast data to them on the
multicast group and port specified. TCP server should run as one thread and
multicasting data run in another thread.

Consists of:
- multicasting object class, init and sender method
- tcp server class, init method and listen method
- Constructor Method. To initialise the server object with a multicast IP and port


Todo:
-need to use the actual multicast group IP e.g. 224.1.1.1

'''

import socket
import threading
import thread
import struct
import time


class multicast_sender(object):
    'Multicasts data to listening clients'

    def __init__(self, multicast_group, multicast_port):
        'Initialise the instance with multicast groups IP and port'
        self.multicast_group = multicast_group
        self.mutlicast_port = multicast_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        'Set socket options, restrict ttl to 1 for now - local segment'
        ttl = struct.pack('b',1) 
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    def sender(self):
        'Method sends data to mutlicast group'
        message = b'This is a message'
        try:
            'Send data here'
            print('sending data {!r}'.format(message))
            sent = self.sock.sendto(message, (self.multicast_group,self.mutlicast_port ))

        finally:
            print('Closing socket...')
            self.sock.close()


    

class tcp_server(object):
    'Listen for TCP connections from clients'

    def __init__(self,ip_address, port):
        'Create and initialise socket for TCP server'
        self.ip_address = ip_address
        self.port = port
        self.clients = 0
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.ip_address, self.port))

    def multi_wrapper(self):
        'Wrapper method to call multicast sender'
        msender = multicast_sender('224.1.1.1',50001)
        msender.sender()
        

    def listener(self):
        'Listen for tcp connections from clients'
        self.sock.listen()
        print('TCP Server listening at {}:{}'.format(self.ip_address,self.port))
        
        while True:
            connected_client, client_address = self.sock.accept()
            self.clients += 1
            print('{} clients connected'.format(self.clients))
            if self.clients == 2:
                thread.start_new_thread(self.multi_wrapper,())    
                


if __name__ == "__main__":
    
    tcp_connection = tcp_server('127.0.0.1',50002)
    thread.start_new_thread(tcp_connection.listener,())
    
