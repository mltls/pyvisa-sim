import logging
import threading

import visa
import time
import json


logging.basicConfig(level=logging.DEBUG)


def worker(dictionary_of_devices):
    import socket
    import sys

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('localhost', 10000)
    print('starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)
    not_done = True
    while not_done:
        # Wait for a connection
        print('waiting for a connection')
        connection, client_address = sock.accept()
        try:
            print('connection from', client_address)

            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(16)
                time.sleep(1)
                print('received {!r}'.format(data))
                if data == b'close':
                    connection.sendall(json.dumps(dictionary_of_devices).encode('utf-8'))
                    not_done = False
                    connection.close()
                    break
                elif data:
                    print('sending data back to the client')
                    connection.sendall(data)
                else:
                    print('no data from', client_address)
                    break

        finally:
            # Clean up the connection
            connection.close()

dict_of_dev = {'devices': {'SR830': {'dialogues': [{'q': '*IDN?',
        'r': 'QCoDeS, Standford Research 830 simulation, 1337, 0.0.01'}],
    'eom': {'GPIB INSTR': {'q': '\r\n', 'r': '\n'}},
    'error': 'ERROR',
    'properties': {'buffer setup': {'getter': {'q': 'SRAT ?', 'r': '13'},
        'setter': {'q': 'SRAT 13', 'r': 'OK'}},
        'change display channel 1': {'getter': {'q': 'DDEF ? 1', 'r': '0, 0'},
        'setter': {'q': 'DDEF 1, 0, 0', 'r': 'OK'}},
        'change display channel 2': {'getter': {'q': 'DDEF ? 2', 'r': '0, 0'},
        'setter': {'q': 'DDEF 2, 0, 0', 'r': 'OK'}},
    'isrc': {'default': '0',
            'getter': {'q': 'ISRC?', 'r': '0'},
            'setter': {'q': 'ISRC {}', 'r': 'OK'}},
            'number of stored points': {'getter': {'q': 'SPTS ?', 'r': '1000'}},
            'pause': {'setter': {'q': 'PAUS', 'r': 'OK'}},
            'reset': {'setter': {'q': 'REST', 'r': 'OK'}},
        'start': {'setter': {'q': 'STRT', 'r': 'OK'}}}}},
    'resources': {'GPIB::1::INSTR': {'device': 'SR830'}},
    'spec': '1.1'}

t = threading.Thread(target=worker, args=(dict_of_dev,))
t.start()
rm = visa.ResourceManager('custom-backend@sim')

r = rm.list_resources()[0]
print(r)
inst = rm.open_resource(r, read_termination='\n')
print(inst.query('*IDN?'))
