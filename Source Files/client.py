import socket
import threading

# A function to handle message sent by clients
def handle_msgs(client,name,ip,port):

    # Joining Group
    client.connect((ip, port))

    print("\n\t\t**Successfully Joined the Group!**\n\t\t\t(Enter Exit to Leave)")
    client.send(name.encode())

    while True:

        # User can either broadcast a message or unicast to a specfic person
        print("\n\t\t\t1-Broadcast\t2-Unicast\n\t\t\t\t  3-Exit")
        opt = input("\n\t\t\t\tSelect: ")

        # sending option selected to middleware
        client.send(opt.encode())

        if opt == "1":
            # Sending Message in Group
            broadcast()

        elif opt == "2":
            # message for a specfic person
            unicast()

        elif opt == "3":
            # Closing Connection
            client.close()

# Function for sending message to all users
def broadcast():

    msg = ""

    while msg != "Exit":

        try:
            msg = client.recv(1024) # if someone is sending message, receive it

        except socket.timeout:  # else, write your own message after timeout

            # Sending message to broadcast
            msg = input("Enter Message: ")
            client.send(msg.encode())

        else:
            # Receiving broadcasted message
            print(">>", msg.decode())

# Function for Receiving a unicast messsage
def unicast():

    flag = 1

    while flag:

        try:
            msg = client.recv(1024)

        except socket.timeout:
            msg = input("\nEnter the Message You want to send: ")
            client.send(msg.encode())

            name = input("\nTo: ")
            client.send(name.encode())
            flag = 0

        else:
            print("$$", msg.decode())
            flag = 0

if __name__ == '__main__':

    # Port Number of user
    port = 9890

    # Creating Client Socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(10) # Setting the timeout value

    # Asking IP from User as Password to Join the Group
    name = input("Enter Your Name: ")
    ip = input("Enter Password to Join Group (127.0.0.1): ")

    while ip != '127.0.0.1':
        print("Wrong Password! Try Again\n")
        ip = input("Enter Password to Join Group (127.0.0.1): ")

    # Using threads for different users
    thread = threading.Thread(target = handle_msgs, args=(client,name,ip,port))
    thread.start()
