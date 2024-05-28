import socket
import poplib

# Proxy server settings
PROXY_PORT = 55555
PROXY_HOST = "localhost"

# Real POP3 server settings
POP3_PORT = 110
POP3_HOST = "localhost"

POP3_USER = "prokingk"
POP3_PASSWORD = "Kapaso123"

# Proxy server credentials
PROXY_USER = "usr"
PROXY_PASSWORD = "pas"

def run_proxy():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy:
        proxy.bind((PROXY_HOST, PROXY_PORT))
        proxy.listen(1)
        print(f"Proxy server listening on {PROXY_HOST}:{PROXY_PORT}")

        while True:
            print("Waiting for a connection...")
            client, address = proxy.accept()
            print(f"Accepted connection from {address}")

            try:
                handle_client(client)
            except Exception as e:
                print(f"Error: {e}")
            finally:
                client.close()

def handle_client(client):
    # Authenticate the client
    client.sendall(b"+OK POP3 proxy server ready\r\n")
    user = receive_line(client)
    if not user.startswith(b"USER " + PROXY_USER.encode()):
        client.sendall(b"-ERR Invalid username\r\n")
        return

    client.sendall(b"+OK\r\n")
    password = receive_line(client)
    if not password.startswith(b"PASS " + PROXY_PASSWORD.encode()):
        client.sendall(b"-ERR Invalid password\r\n")
        return

    client.sendall(b"+OK Authenticated\r\n")

    # Connect to the real POP3 server
    pop3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    pop3.connect((POP3_HOST, POP3_PORT))
    response = pop3.recv(4096)
    print(response.decode())

    pop3.sendall(b'USER ' + POP3_USER.encode() + b'\r\n')
    response = pop3.recv(4096)
    print(response.decode())

    pop3.sendall(b'PASS ' + POP3_PASSWORD.encode() + b'\r\n')
    response = pop3.recv(4096)
    print(response.decode())

    # Relay commands between the client and the real server
    while True:
        client_command = receive_line(client)
        print(f"Client command: {client_command.decode().rstrip()}")

        if client_command.upper().startswith(b"QUIT"):
            client.sendall(b"+OK Bye\r\n")
            pop3.close()
            break

        pop3.sendall(client_command + b'\n')
        response = pop3.recv(4096)
        client.sendall(response)

        if client_command.upper().startswith(b"RETR"):
            data = b''
            while True:
                chunk = pop3.recv(4096)
                if chunk.endswith(b'.\r\n'):
                    data += chunk[:-3]
                    break
                data += chunk
            client.sendall(data + b'\r\n.\r\n')

def receive_line(socket):
    data = b""
    while True:
        chunk = socket.recv(1)
        if chunk == b"\n":
            return data
        data += chunk

if __name__ == "__main__":
    run_proxy()