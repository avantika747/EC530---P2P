PEER-TO-PEER MESSAGING CHATROOM

This is an implementation of a P2P messaging chatroom. 

The central server acts as a chatroom for anyone who connects to that network. It can be thought of as an implementation of a WhatsApp/Telegram group chat. The server initiates the connection, and each of the clients can communicate with one another. It has a simple command line interface for interaction. 

Initializing the server:

python p2pserver.py server --ip <<IP_ADDRESS>> --port <<PORT_NUMBER>>

Initializing each client:

python p2pclient.py client --username <<USERNAME>> --ip <<SERVER_IP>> --port <<SERVER_PORT>>

Once connected to the common port, each client has access to the chatroom to send and receive messages. Once connected, clients can send messages to other connected users by specifying the recipient's username along with the message content.

To close the connection, simply close the terminal window. 

Implementation examples:
![image](https://github.com/avantika747/EC530---P2P/assets/66120758/03a0082d-60b1-451b-91c8-ad411151ec55)






