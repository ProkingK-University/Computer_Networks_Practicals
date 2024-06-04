import socket
import datetime
import threading

# POP3 PROXY
POP3_PROXY_PORT = 12345
POP3_PROXY_HOST = "localhost"

POP3_PROXY_USER = "prokingk@localhost"
POP3_PROXY_USER_2 = "admin@localhost"
POP3_PROXY_PASSWORD = "pas"

# SMTP PROXY
SMTP_PROXY_PORT = 54321
SMTP_PROXY_HOST = "localhost"

SMTP_PROXY_USER = "prokingk@localhost"
SMTP_PROXY_PASSWORD = "pas"

# POP3
POP3_PORT = 110
POP3_HOST = "localhost"

POP3_USER = "prokingk"
POP3_PASSWORD = "Kapaso123"

# SMTP
SMTP_PORT = 25
SMTP_HOST = "localhost"

ALLOWED_DELETE_USER = "admin@localhost"

def run_pop3_proxy():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy:
        proxy.bind((POP3_PROXY_HOST, POP3_PROXY_PORT))
        proxy.listen(1)
        print(f"Proxy server listening on {POP3_PROXY_HOST}:{POP3_PROXY_PORT}")

        while True:
            print("Waiting for a connection...")
            client, address = proxy.accept()
            print(f"Accepted connection from {address}")

            try:
                handle_pop3_client(client)
            except Exception as e:
                print(f"Error: {e}")
            finally:
                client.close()

def run_smtp_proxy():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((SMTP_PROXY_HOST, SMTP_PROXY_PORT))
        server_socket.listen(1)
        print(f"SMTP proxy server listening on {SMTP_PROXY_HOST}:{SMTP_PROXY_PORT}")

        while True:
            print("Waiting for a connection...")
            client, address = server_socket.accept()
            print(f"Accepted connection from {address}")

            try:
                handle_smtp_client(client)
            except Exception as e:
                print(f"Error: {e}")
            finally:
                client.close()

def handle_smtp_client(client):

    # Connect to SMTP server
    smtp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    smtp.connect((SMTP_HOST, SMTP_PORT))
    response = smtp.recv(4096)
    client.sendall(response)
    print(response.decode())

    # Relay commands
    while True:
        client_command = receive_line(client)
        print(f"Client command: {client_command.decode().rstrip()}")

        if client_command.startswith(b"QUIT"):
            client.sendall(b"+OK Bye\r\n")
            smtp.close()
            break
        
        if client_command.startswith(b'DATA'):
            smtp.sendall(client_command + b'\n')
            response = smtp.recv(4096)
            client.sendall(response)
            data = b''
            while True:
                chunk = client.recv(4096)
                if chunk.endswith(b'.\r\n'):
                    data += chunk[:-3]
                    break
                data += chunk
            smtp.sendall(data + b'\r\n.\r\n')
            response = smtp.recv(4096)
            print('SMTP response:', response.decode())
            client.sendall(response)
            continue

        smtp.sendall(client_command + b'\n')
        response = smtp.recv(4096)
        print('SMTP response:', response.decode())
        client.sendall(response)

def handle_pop3_client(client):
    # Authenticate client
    client.sendall(b"+OK POP3 proxy server ready\r\n")
    user = receive_line(client)
    print(user.decode())
    client.sendall(b"-ERR Unknown command\r\n")
    
    user = receive_line(client)
    print(user.decode())
    array = user.split(b" ")
    username = array[1].decode().rstrip()
    print('USER ' + username)
    if not (user.startswith(b"USER " + POP3_PROXY_USER.encode()) or user.startswith(b"USER " + POP3_PROXY_USER_2.encode())):
        client.sendall(b"-ERR Invalid username\r\n")
        return

    client.sendall(b"+OK\r\n")
    password = receive_line(client)
    if not password.startswith(b"PASS " + POP3_PROXY_PASSWORD.encode()):
        client.sendall(b"-ERR Invalid password\r\n")
        return

    client.sendall(b"+OK Authenticated\r\n")

    # Connect to POP3 server
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
    
    print('Before While: ' + username)

    # Relay commands
    while True:
        client_command = receive_line(client)
        print(f"Client command: {client_command.decode().rstrip()}")
        
        print('After While: ' + username)

        if client_command.startswith(b"QUIT"):
            client.sendall(b"+OK Bye\r\n")
            pop3.close()
            break
        
        
        if client_command.upper().startswith(b"DELE"):
            if username == ALLOWED_DELETE_USER:
                client.sendall(response)
                print("Email deleted")
            else:
                client.sendall(b"-ERR Permission denied\r\n")
                print('Delete declined')

        pop3.sendall(client_command + b'\n')
        response = pop3.recv(4096)
        
        # Log the email download
        if client_command.upper().startswith(b"RETR"):
            subject_lines = [line.decode() for line in response.split(b"\r\n") if line.decode().startswith("Subject:")]
            
            if subject_lines:
                email_subject = subject_lines[0][9:].strip()
            else:
                email_subject = "Unknown"

            log_email_download(username, email_subject)
            print('Logged')
        
        if client_command.upper().startswith(b"RETR"):
            response_lines = response.split(b"\r\n")

            for i, line in enumerate(response_lines):
                # Handel Email
                if line.decode().startswith("Date:"):
                    response_lines.insert(i + 2, b"Handled by " + username.encode())
                    print('Handel inserted')
                    break
                if line.decode().startswith("Subject: Confidential"):
                    response_lines[i] = b"Subject: Just testing"
                    response_lines[i + 5] = b"This is a cover email."
                    print('Email hidden')
                    break

            response = b"\r\n".join(response_lines)
            
        client.sendall(response)

def receive_line(socket):
    data = b""
    while True:
        chunk = socket.recv(1)
        if chunk == b"\n":
            return data
        data += chunk

def log_email_download(username, email_subject):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} | {username} | Downloaded email: {email_subject}"
    with open("email_download_log.txt", "a") as log_file:
        log_file.write(log_entry + "\n")

def run_proxies():
    pop3_thread = threading.Thread(target=run_pop3_proxy)
    smtp_thread = threading.Thread(target=run_smtp_proxy)

    pop3_thread.start()
    smtp_thread.start()

    pop3_thread.join()
    smtp_thread.join()

if __name__ == "__main__":
    run_proxies()