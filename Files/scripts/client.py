#Ross Bathgate
#Learning Socket

#NOTE: See the files under ./old/ for more internal commentary

import socket
import threading
import chatModule as cm

HEADER = 64
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SEND_RESPONSE_MESSAGE = "!RESPOND"
CHECK_USER_MESSAGE = "!USER"
SERVER = "00.00.00.00"  # Enter IP Address of server device here
ADDR = (SERVER,PORT)
local_username = "___"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

messageHistoryList = []
currentMsgCount = 0

latest_message_id = 0

threadStarted = False

OWN_MSG_FILL = (164,164,164)
OTHER_MSG_FILL = (103,234,119)

BOTTOM_MOST_Y = 903
TOP_MOST_Y = 150
MSG_GAP = 20

LINE_LENGTH_LIMIT = 33
MAX_NUM_LINES = 5
MAX_DISPLAY_LINES = 3

#connect to server
try:
    client.connect(ADDR)
except Exception as e:
    print("Failed to connect to server")
    input("OK?")
    quit()

def play_sound(pathToSound):
    pygame.mixer.init()
    pygame.mixer.music.load(pathToSound)
    pygame.mixer.music.play()

#send message function
def send(msg):
    if len(msg) > 0:
        message = (local_username + ">" + msg).encode(FORMAT)
        msg_length = len(message)

        #send this to the server to determine the number of bytes of the next message
        send_length_msg = str(msg_length).encode(FORMAT)

        #pad out to 64 bytes (defined on server)
        send_length_msg += b" " * (HEADER - len(send_length_msg))

        #now send the messages
        client.send(send_length_msg)
        client.send(message)

def recreate_msg_list(msg):
    all_messages = msg.split("#")
    return [all_messages[i].split("$") for i in range(len(all_messages) - 1)] #the last element is always an empty string so ignore it

def store_messages(messages):
    global currentMsgCount
    global messageHistoryList
    messageHistoryList = []

    for message in messages:
        _id, addr, contents = message
        user,text = contents.split(">")
        messageHistoryList.append((user,text,_id))

        if len(messageHistoryList) > currentMsgCount:
            currentMsgCount = len(messageHistoryList)
            play_sound("../media/sounds/newMsg.mp3")

def receive_response():
    global threadStarted
    send(SEND_RESPONSE_MESSAGE)
    #receive response
    msg_length = client.recv(HEADER).decode(FORMAT)

    #if msg_length: #check if not NONE
    if msg_length and msg_length[0] != 0:
        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(FORMAT)
        store_messages(recreate_msg_list(msg))
        threadStarted = False

def receive_response_user(username):
    send(CHECK_USER_MESSAGE + "." + str(username))
    #receive response
    msg_length = client.recv(HEADER).decode(FORMAT)

    #if msg_length: #check if not NONE
    if msg_length and msg_length[0] != 0:

        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(FORMAT)


        if msg != (CHECK_USER_MESSAGE + ".True") and msg != (CHECK_USER_MESSAGE + ".False"):
            store_messages(recreate_msg_list(msg))
        else:
            return (msg)

#checks if username is already taken
def assign_username(username):
    response = receive_response_user(username)
    if response == (CHECK_USER_MESSAGE + ".True"):
        return True
    elif response == (CHECK_USER_MESSAGE + ".False"):
        return False
    else:
        print("ERROR - incorrect response.  Response was:",response)
        quit()



#----------pygame settings----------
input_text = ""

def refresh_display():
    window.fill((255,255,255))
    img = pygame.image.load("../media/images/chat_main_background.png")
    window.blit(img, (0,0))

    #---Create list of msg()---
    if len(messageHistoryList) > 0:
        #create new empty list to store all messages
        #smaller index is a more recent message
        display_messages = []

        #extract details of the most recent message
        user, text, _id = messageHistoryList[-1]

        #create the most recent message
        display_messages.append(cm.msg(0,OWN_MSG_FILL if user == local_username else OTHER_MSG_FILL, text, user if user != local_username else "You", _id, (user == local_username)))

        #now alter the y attribute of the above message
        #could not do this before since the height is calculated during object creation
        display_messages[-1].y = BOTTOM_MOST_Y - display_messages[-1].h - MSG_GAP

        #create all other messages:
        #create a new list which is the reverse of messageHistoryList
        #i.e. index 0 is the most recent
        holdMessageList = messageHistoryList[::-1] #reverse

        #loop through each index after the first index and create a new message as above
        if len(holdMessageList) > 1:
            for i in range(1, len(holdMessageList)):
                user, text, _id = holdMessageList[i]
                display_messages.append(cm.msg(0,OWN_MSG_FILL if user == local_username else OTHER_MSG_FILL, text, user if user != local_username else "You", _id, (user == local_username)))

                #alter the y value based on the previous message
                display_messages[-1].y = display_messages[-2].y - display_messages[-2].h - MSG_GAP

        #only draw messages which will fit on the screen.
        for m in display_messages:
            if m.y > TOP_MOST_Y:
                m.draw()


    #display the text in the textbox
    msgTbx.display_text(MAX_DISPLAY_LINES)

    #draw the send button
    send_btn.draw()

    pygame.display.update()


# -------- MAIN PROGRAM --------

import pygame
pygame.init()
window = pygame.display.set_mode((800,1000))
pygame.display.set_caption('Chat   |   By Ross Bathgate')


#ask user for username etc.

#create a text box for entering username:
userTbx = cm.textbox(0,BOTTOM_MOST_Y, 800,pygame.display.get_surface().get_size()[1] - BOTTOM_MOST_Y,"Start typing a username...")

#create a 'submit' button
submitUser_btn = cm.button(700,BOTTOM_MOST_Y, 100,pygame.display.get_surface().get_size()[1] - BOTTOM_MOST_Y,(80,128,85),"OK")


errorText = ""
def start_up_display():
    window.fill((255,255,255))
    img = pygame.image.load("../media/images/chat_start_background.png")
    window.blit(img, (0,0))

    #error text
    font = pygame.font.SysFont('Arial', 30)
    text = font.render(errorText, False, (255,0,0))
    window.blit(text,(0,BOTTOM_MOST_Y-150))

    userTbx.display_text(1)
    submitUser_btn.draw()

    pygame.display.update()

#--- start up procedure ---
startup = True
run = True

while startup:
    userTbx.text = input_text
    start_up_display()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            startup = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            elif event.key == pygame.K_RETURN:
                if assign_username(input_text):
                    local_username = input_text
                    startup = False
                else:
                    errorText = "Username taken."
            else:
                if len(input_text) < (LINE_LENGTH_LIMIT // 1.8):
                    if (event.unicode not in ("#","$",">")):
                        input_text += event.unicode
                        userTbx.text = input_text
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if submitUser_btn.clicked(mouse_pos):
                if assign_username(input_text):
                    local_username = input_text
                    startup = False
                else:
                    errorText = "Username taken."



#--- main chat screen ---

#reset the input_text variable to be an empty string
input_text = ""

#create a text box for entering messages:
msgTbx = cm.textbox(0,BOTTOM_MOST_Y, 800,pygame.display.get_surface().get_size()[1] - BOTTOM_MOST_Y,"Start typing a message...")

#create a 'send' button
send_btn = cm.button(700,BOTTOM_MOST_Y, 100,pygame.display.get_surface().get_size()[1] - BOTTOM_MOST_Y,(89,200,255),"SEND")

refresh_display()

#----------main program----------
while run:
    if not threadStarted:
        threadStarted = True
        thread = threading.Thread(target = receive_response)
        thread.start()

    msgTbx.text = input_text
    refresh_display()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            elif event.key == pygame.K_RETURN:
                if input_text not in (DISCONNECT_MESSAGE, SEND_RESPONSE_MESSAGE, CHECK_USER_MESSAGE):
                    if not input_text.isspace(): #don't send if all whitespace
                        send(input_text)
                input_text = ""
                #threadStarted = False
            else:
                if len(input_text) < (LINE_LENGTH_LIMIT * MAX_NUM_LINES):
                    if (event.unicode not in ("#","$",">")):
                        input_text += event.unicode
                        msgTbx.text = input_text


        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if send_btn.clicked(mouse_pos):
                if input_text not in (DISCONNECT_MESSAGE, SEND_RESPONSE_MESSAGE, CHECK_USER_MESSAGE):
                    if not input_text.isspace(): #don't send if all whitespace
                        send(input_text)
                input_text = ""

send(DISCONNECT_MESSAGE)
