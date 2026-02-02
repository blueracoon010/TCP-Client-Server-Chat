# TCP-Client-Server-Chat
A TCP-based client-server chat system in Python using sockets, supporting concurrent clients, session tracking, and acknowledgment-based messaging

##  Setup and Usage

###  Requirements
- Python 3.10.6 or 3.12.0
- No external libraries required

###  Running the Server
1. Open a terminal window
2. Navigate to the project directory
3. Start the server:
```bash
   python server.py
```
4. The server will begin listening for client connections on `localhost:5050`

###  Running the Client(s)
1. Open a new terminal window for each client (supports up to 3 simultaneous connections)
2. Start a client:
```bash
   python client.py
```
3. Once connected, you can begin typing messages

###  Available Commands
- `list` — List available files on the server
- `get <filename>` — Download a file from the server
- `exit` — Disconnect from the server