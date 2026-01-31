import socket 
import threading
import itertools
from datetime import datetime
import os

HEADER = 64     # Fixed-size header to store message length
PORT= 5050      
SERVER =  socket.gethostbyname(socket.gethostname()) # Dynamically retrieves host IP (IPv4)
ADDR = (SERVER,PORT)   #stored as tuple
FORMAT='utf-8'     # Encoding format for message transfer
CLOSE_MESSAGE="exit"  # signals  client disconnection

#socet.socket() makes a new socket , 
#this accepts socket.AF_INET as the frist argument ->  ipv4 address family
#socket.Sock_STream is the second argument -> strream based (tcp)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(ADDR)   #binding the sockets to  server 

client_counter = itertools.count(1)   #auto-assign client names (Client01, Client02, etc.)

clients_cache = {}             #cache to store accepted clients with timestamps

MAX_CLIENTS = 3               #sets maximumum client count to 3
active_clients = 0
lock = threading.Lock()


REPO_DIR = "./repo"           #repo for file listing
os.makedirs(REPO_DIR, exist_ok=True)



# the function assign_name() produces  a sequential name for each client (Client01, Client02...)
def assign_name():
    num = next(client_counter)
    return f"Client{num:02d}"


#the function handle_client() handles all communication with a single connected client.
#Runs in a dedicated thread to support multiple concurrent users.
#arguments : conn , addr, clieint_name

def handle_client(conn, addr, client_name):  # runs for each client concurrently 
    global active_clients
    print(f"[NEW CONNECTION] {client_name} {addr} connected")

    # stores acceptance time fro tracking session times 
    clients_cache[client_name] = {
        "accepted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),     # records start time
        "finished_at": None
    }
    connected = True           # flag that indicates the connection is true 
    while connected:    
        #blockng line of code :  waits for client message length (won’t proceed until data is received)
        msg_len = conn.recv(HEADER).decode(FORMAT)   
        if msg_len:                 # proceed only if some data was received
            msg_len= int(msg_len)   #converts to int 
            msg = conn.recv(msg_len).decode(FORMAT)  #recieves message

            if msg.lower() == CLOSE_MESSAGE:   #handling client disconnection
                connected = False

            print(f"[{client_name}] {msg}")    # log the message received from the client

           
            # the following logic is added for bonus, it handles file commands
            if msg.lower() == "list":        #client requests files 
                files = os.listdir(REPO_DIR)   #gets files
                response = "Files: " + ", ".join(files) if files else "No files found."
                conn.send(response.encode(FORMAT))   #returns the list 


            elif msg.lower().startswith("get "):  #request to download
                filename = msg.split(" ", 1)[1]    #gets filename
                filepath = os.path.join(REPO_DIR, filename)   #build file path 

                if not os.path.exists(filepath):   #logic for missing file 
                    conn.send("ERR: File not found".encode(FORMAT))  
                else:
                    with open(filepath, "rb") as f:  #opens file in binary
                        content = f.read()
                    conn.send(content)                  #returns the content of the file
            else:
                conn.send(f"ACK {msg}".encode(FORMAT))  # default acknowledgment messages

    conn.close()   # closes connection after client disconnects

  # stores disconnect time
    clients_cache[client_name]["finished_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #  decrements active client count
    with lock:
        active_clients -= 1
    print(f"[DISCONNECTED] {client_name}. Active clients now: {active_clients}")   

#hndles new connections and distribute where it goes 
#starts the server and listens for new client connections
def start():
    global active_clients
    server.listen() #listenign clients 
    print("[LISTENING] SERVER IS LISTENING ON", {SERVER})


    while True:
        conn, addr  = server.accept() #when a new connection occurs we store the addr and the object conn
             #limits concurrent clients
        with lock:
            if active_clients >= MAX_CLIENTS:
                conn.send("Server busy. Try later.".encode(FORMAT))
                conn.close()
                continue
            active_clients += 1
        
        #  assigns client name automatically
        client_name = assign_name()
        print(f"{client_name} connected from {addr}")
        
        # creates a new thread for each client 
        thread = threading.Thread(target=handle_client,args=(conn,addr,client_name))
        thread.start()    # start the client thread
         # prints the number of active client connections (threads)
        print(f"[active connections]{threading.active_count()-1}")


print("SERVER IS STARTING")
start()
