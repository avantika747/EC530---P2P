import sqlite3
import socket
import threading
import argparse

# Naming the database file
db_file = "p2pmessaging.db"

class Peer:
    def __init__(self, username, ip, port):
        self.username = username
        self.ip = ip
        self.port = port

class P2PChat:
    def __init__(self, username, ip, port):
        self.username = username
        self.ip = ip
        self.port = port
        self.peers = []
        self.messages = []

        # Connect to the database
        self.db_connection = sqlite3.connect(db_file)
        self.create_tables()

        # Create the server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(5)

    def create_tables(self):
        cursor = self.db_connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY,
            sender TEXT,
            recipient TEXT,
            message TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        self.db_connection.commit()

    def handle_peer(self, client_socket, addr):
        username = client_socket.recv(1024).decode("utf-8")
        peer = Peer(username, addr[0], addr[1])
        self.peers.append(peer)
        print(f"User '{username}' connected from {addr[0]}:{addr[1]}")

        while True:
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                recipient, message_content = message.split(":")
                self.messages.append((username, recipient, message_content))
                self.save_message(username, recipient, message_content)
                print(f"Message sent from '{username}' to '{recipient}': {message_content}")
                self.send_message(recipient, f"{username}: {message_content}")

    def save_message(self, sender, recipient, message):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO messages (sender, recipient, message) VALUES (?, ?, ?)",
                       (sender, recipient, message))
        self.db_connection.commit()

    def send_message(self, recipient, message):
        for peer in self.peers:
            if peer.username == recipient:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sender_socket:
                    sender_socket.connect((peer.ip, peer.port))
                    sender_socket.send(message.encode("utf-8"))

    def start(self):
        print(f"Server started at {self.ip}:{self.port}")
        while True:
            client_socket, addr = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_peer, args=(client_socket, addr))
            client_thread.start()
class P2PClient:
    def __init__(self, username, ip, port):
        self.username = username
        self.ip = ip
        self.port = port

    def send_message(self, recipient, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.ip, self.port))
            client_socket.send(f"{self.username}:{recipient}:{message}".encode("utf-8"))

def main():
    parser = argparse.ArgumentParser(description="P2P Messaging System")
    parser.add_argument("role", choices=["server", "client"], help="Choose 'server' or 'client'")
    parser.add_argument("--ip", default="127.0.0.1", help="IP address to bind/connect to")
    parser.add_argument("--port", type=int, default=12345, help="Port number to bind/connect to")
    parser.add_argument("--username", help="Username for the client")

    args = parser.parse_args()

    if args.role == "server":
        # Start server code
        pass
    elif args.role == "client":
        if not args.username:
            parser.error("You must provide a username for the client")

        client = P2PClient(args.username, args.ip, args.port)

        while True:
            recipient = input("Enter recipient username: ")
            message = input("Enter message: ")

            if recipient and message:
                client.send_message(recipient, message)
            else:
                print("Recipient or message cannot be empty.")
                continue

if __name__ == "__main__":
    main()
