'''
Name:  Marc Smith
Date:  2017-02-14
Description:
A multithreaded multicast server that listens for connections from clients on the
multicast group and port specified and spawns a new connection to handle the
client connection.

Consists of:
- server class
- Constructor Method. To initialise the server object with a multicast IP and port
- listen method. To listen for connections from clients
- Client_handler method. Will do the required heavy lifting

Todo:
-clean up comments
-clients variable is used to track the number of connected clients
will use this to know when the required number of clients connect
to start multicasting data.
-complete the client handler method to do the heavy lifting
-need to use the actual multicast group IP e.g. 224.1.1.1

'''

import socket
import threading
import struct
import time

class server(object):
    'Multithreaded multicast server to allow clients to connect'

    def __init__(self, multicast_group, multicast_port):
        'Initialise the instance with a multicast IP address and port number'
        'Set the socket options'
        self.clients = 0                                                
        self.multicast_group = ''               #multicast_group address. Need use real multicast address eventually
        self.multicast_port = multicast_port    #multicast_port
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)    #Create UDP socket
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.multicast_group, self.multicast_port))  #Bind the socket (sock) to the host and port
        mreq = struct.pack("4sl", socket.inet_aton(multicast_group), socket.INADDR_ANY)

        'Set option to join multicast group'
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        
    def listen(self):
        'Listens for connections from clients and spawns a new thread'        
        bufsize = 1024
        
        print('Server listening on {}:{}'.format(self.multicast_group,self.multicast_port))              
        while True:
            'Need to double check using recv() or recvfrom() here'
            connected_client, client_address = self.sock.recvfrom(bufsize)            
            'Spawn thread with the client_handler method'
            threading.Thread(target = self.client_handler, args = (connected_client, client_address)).start()
            self.clients += 1
            print('{} clients connected'.format(self.clients))


    def client_handler(self, connected_client, client_address):
        'For now the method sends the time to the client, for testing purposes'
        size = 1024
        
'''         while True:
            'Send the time to the client'
            now = time.localtime()
            sent_data = time.strftime('%H:%M',now)
            
            connected_client.sendto(sent_data)
            'This is for testing, TAKEOUT!'
            print(sent_data)
                
'''           


if __name__ == "__main__":
    addr = input('Enter multicast address: ')
    port = eval(input('Enter port number to use: '))
    server(addr,port).listen()
