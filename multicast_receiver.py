import socket
import struct

class multicast_receiver(object):
    'Listens for multicast stream'

    def __init__(self, multicast_group, multicast_port):
        'Initialise the instance with multicast groups IP and port'
        self.multicast_group = multicast_group
        self.mutlicast_port = multicast_port
        self.data_size = 0
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.bind(('',50001))

        'Set socket options'
        mreq = struct.pack('4sL', socket.inet_aton(multicast_group), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        

    def receive(self):
        while True:
            print('\nWaiting to receive data...')
            data, address = self.sock.recvfrom(1024)

            self.data_size = len(data)
            print('Received {} bytes from {}'.format(self.data_size, address))
            
class tcp_connector(object):
    'Send feedback to multicast sender via tcp'

    def __init__(self):
        self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def sender(self,host,port):
        'TCP sender (client) to provide feedback'
        data = 'Ready To receive data'
        self.tcp_sock.connect((host, port))
        self.tcp_sock.sendall(b'data')



if __name__ == "__main__":
    #tcp_connection = tcp_connector()
    #tcp_connection.sender('127.0.0.1',50002)
    

    mreceiver = multicast_receiver('224.1.1.1',50001)
    mreceiver.receive()
