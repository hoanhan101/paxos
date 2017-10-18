#!/usr/bin/env python3
"""
    client_multi_thread.py - UDP client multi-thread
    Author: Hoanh An (hoanhan@bennington.edu)
    Date: 10/16/2017
"""

import threading
import socket

UDP_ADDRESS = '127.0.0.1'
UDP_PORT = 9000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

clients = {}



class Client(threading.Thread):
    def __init__(self, task):
        threading.Thread.__init__(self)
        self.task = task
        self.permitted_id = "(1,\'A\')"
        self.accepted_id = "(1,\'A\')"
        self.accepted_value = "Foo"

    def send(self):
        # message = "PERMISSION-REQUEST_(2,\'A\')"  PERMISSION-REQUEST_(9,'A')
        #
        # s.sendto(message.encode(), (UDP_ADDRESS, UDP_PORT))
        # print("SENT {0} TO {1}".format(message, UDP_ADDRESS))

        while True:
            message = input(">> ")

            s.sendto(message.encode(), (UDP_ADDRESS, UDP_PORT))
            print("SENT {0} TO {1}".format(message, UDP_ADDRESS))

    def receive(self):
        print(self.permitted_id, self.accepted_id, self.accepted_value)
        while True:
            data, addr = s.recvfrom(1024)
            data = data.decode()

            print("RECEIVE {0} FROM: {1}".format(data, addr[0]))

            new_data = split_string(data, '_')
            if new_data[0] == "PERMISSION-GRANTED":
                self.permitted_id = new_data[1]
                # NEED TODO SOMETHING WITH ACCEPTED ID AND VALUE
                message = "SUGGESTION_{0}_{1}".format(self.permitted_id, self.accepted_value)

                s.sendto(message.encode(), (UDP_ADDRESS, UDP_PORT))
                print("SENT {0} TO {1}".format(message, UDP_ADDRESS))
            elif new_data[0] == "ACCEPTED":
                self.accepted_id = new_data[1]
                print("DONE")
                print(self.permitted_id, self.accepted_id, self.accepted_value)
            elif new_data[0] == "PERMISSION-REQUEST":
                if self.permitted_id < new_data[1]:
                    self.permitted_id = new_data[1]

                    message = "PERMISSION-GRANTED_{0}_{1}_{2}".format(self.permitted_id, self.accepted_id, self.accepted_value)

                    s.sendto(message.encode(), (UDP_ADDRESS, UDP_PORT))

            elif new_data[0] == "SUGGESTION":
                if self.permitted_id <= new_data[1]:
                    self.permitted_id = new_data[1]
                    self.accepted_id = new_data[1]
                    self.accepted_value = new_data[2]

                    message = "ACCEPTED_{0}".format(self.permitted_id)

                    s.sendto(message.encode(), (UDP_ADDRESS, UDP_PORT))
                    print(self.permitted_id, self.accepted_id, self.accepted_value)


    def run(self):
        # print("START {0}_THREAD".format(self.task))
        if self.task == "SEND":
            self.send()
        else:
            self.receive()
        # print("FINISHED {0}_THREAD".format(self.task))


def split_string(string, delimeter):
    string_array = string.split(delimeter)
    return string_array

def is_first_id_larger(id_1, id_2):
    if int(id_1[0]) >= int(id_2[0]) and ord(id_1[1]) >= ord(id_2[1]):
        return True
    else:
        return False

if __name__ == '__main__':
    threading_lock = threading.Lock()
    threads = []

    SEND_THREAD = Client("SEND")
    RECEIVE_THREAD = Client("RECEIVE")

    SEND_THREAD.start()
    RECEIVE_THREAD.start()

    threads.append(SEND_THREAD)
    threads.append(RECEIVE_THREAD)

    for thread in threads:
        thread.join()

    print("DONE")