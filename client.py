import socket 

#Defining constants for message formatting

HEADER = 64        
PORT= 5050          
FORMAT='utf-8'
CLOSE_MESSAGE="exit"
SERVER =  socket.gethostbyname(socket.gethostname()) 
ADDR= (SERVER,PORT)

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)


    

# The follwing send() function takes in 
# argument : msg 
# and sends the length of the message with the actual encoded messge 

def send(msg):
    message= msg.encode(FORMAT)     # encodes message string into bytes using the utf-8 format
    msg_len= len(message)
    send_len = str(msg_len).encode(FORMAT)    # encodes the length into bytes(so it can be sent through sockets )
    send_len += b' ' * (HEADER - len(send_len))  # pads the length header with spaces to make it a fixed size 
    client.send(send_len)
    client.send(message)


print("Connected to server. Type your messages below:")
print("Type 'list' to see available files or 'get <filename>' to download one.")
print("Type 'exit' to disconnect.")
while True:
    msg = input("> ")  # CLI input
    send(msg)
    if msg.lower() == CLOSE_MESSAGE:
        break
    # receive ACK from server
    response = client.recv(2048).decode(FORMAT)
    print(response)
client.close()