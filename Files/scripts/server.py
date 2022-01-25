#Ross Bathgate
#Learning Socket

import socket
import threading
import time

PORT = 5050
SERVER = ""# socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SEND_RESPONSE_MESSAGE = "!RESPOND"
CHECK_USER_MESSAGE = "!USER"

messages = []
message_count = 0

usernames = []

#socket server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create new socket.  AF_INET = the type of IP that is being accepted....  STEAM = the way data is being sent
server.bind(ADDR)


def send(msg, con):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length_msg = str(msg_length).encode(FORMAT)
    send_length_msg += b" " * (HEADER - len(send_length_msg))
    con.send(send_length_msg)
    con.send(message)

def convert_msg_list():
    string = ""
    for message in messages:
        id, addr, msg = message
        string += (str(id) + "$" + str(addr) + "$" + msg + "#")

    return string


def handle_client(con, addr):
    global messages
    global usernames
    global message_count
    print("{NEW CONNECTION}", addr)

    connected = True
    while connected:
        msg_length = con.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            #receive actual message
            _msg_ = con.recv(msg_length).decode(FORMAT) #connection.receive(#bytes)

            msg = _msg_.split(">")[1] #get rid of the username

            if msg == DISCONNECT_MESSAGE:
                connected = False

            elif msg == SEND_RESPONSE_MESSAGE:
                #send a message back to client (call send() above)
                return_msg = convert_msg_list()
                send(return_msg,con)

            #checks if the new user's name already exists or not
            elif msg[:len(CHECK_USER_MESSAGE)] == CHECK_USER_MESSAGE:
                username = msg[len(CHECK_USER_MESSAGE)-1:]
                if username not in usernames:
                    usernames.append(username)
                    send((CHECK_USER_MESSAGE + ".True"),con)
                else:
                    send((CHECK_USER_MESSAGE + ".False"),con)

            else:
                message_count += 1
                messages.append((message_count,addr,(_msg_)))



        #print what the message is
        print(str(time.asctime(time.localtime(time.time()))) + ": " + "client{"+str(addr)+"} says -->",msg)

    con.close() #disconnect the current connection after the DISCONNECT_MESSAGE is received



def start(): #start socket server
    #listen for new connections
    server.listen()
    print("{SERVER IS LISTENING ON}", SERVER)

    while True: #infinite loop
        #wait on this line until a new connection is made
        con, addr = server.accept() #addr is the port and ip, con is the connection object

        #start a new thread equal to the handle_client
        thread = threading.Thread(target = handle_client, args = (con, addr))

        #start the thread
        thread.start()

        #[optional...] print the number of active connections
        print("{ACTIVE CONNECTIONS}", threading.activeCount() - 1) #-1 because there is always one thread running


#main program
print("{SERVER IS STARTING}")
start()
