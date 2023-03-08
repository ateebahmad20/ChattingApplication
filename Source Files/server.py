import socket
import threading
import time

# max length of msg in bytes
size = 1024

# Function for Broadcasting message in group
def broadcast(user,users_dict,name):
    msg = ""

    # While user is in the Group, broadcast message
    while msg != "Exit":

        # Receiving and decoding messages
        msg = user.recv(size)
        print("Broadcast =>", name.decode(),": ", msg.decode())
        str = name.decode() + ": " + msg.decode() + "\n"
        str = str.encode()

        # Broadcasting msg to all users
        for i in range(len(users_dict)):
            conn[i].send(bytes(str))

    print("\n*", name.decode(), "Left the group")

# Function to send message to a particular user
def unicast(user,sender):

    index = -1

    # Receiving message from user
    msg = user.recv(size)
    receiver = user.recv(size)

    # Storing message in middleware
    print("Unicast =>", sender.decode(),": ", msg.decode())

    # Creating a new message to send
    str = sender.decode() + ": " + msg.decode() + "\n"
    str = str.encode()

    # Searching for person in dictionary
    for user in users_dict:
        if(user == receiver.decode()):
            break

        else:
            index += 1

    # Sending to the required user
    conn[index+1].send(bytes(str))

# A function to handle user's messages
def handle_clients(user, address):

    name = user.recv(size)

    # Storing user info in dictionary
    users_dict[name.decode()] = address[1]

    print("\n*", name.decode(), "Joined the Group")

    while True:

        # Receiving option status from user
        opt = user.recv(size)
        opt = opt.decode()

        if opt == '1':
            broadcast(user,users_dict,name)

        elif opt == '2':
            unicast(user,name)

if __name__ == '__main__':

    # Loopback IP Address and Port Number for Group
    ip = "127.0.0.1"
    port = 9890
    users_dict = {} # dictionary to keep track of all Users
    conn = []

    # Creating Group/Server Socket
    group = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Binding socket with Respective IP and Port
    group.bind((ip, port))

    print("\t\t**Group Created!**\n")
    print("Waiting for Users to Join...")

    group.listen() # listening for users

    while True:
        user, address = group.accept()

        conn.append(user)

        # Creating different users as threads
        thread = threading.Thread(target = handle_clients, args=(user, address))
        thread.start()

    # Closing Connections:
    user.close()
    group.close()
