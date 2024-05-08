import socket

get_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
send_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

get_server.connect(('localhost', 110))
get_server.recv(4096)

get_server.send(b'USER prokingk\n')
get_server.recv(4096)
get_server.send(b'PASS Kapaso123\n')
get_server.recv(4096)

get_server.send(b'LIST\n')
get_server.recv(4096)
get_server.send(b'RETR 1\n')

email = get_server.recv(4096)
print(email.decode())

get_server.close()

send_server.connect(('localhost', 25))
send_server.recv(4096)

send_server.send(b'HELO localhost\n')
send_server.recv(4096)
send_server.send(b'MAIL FROM: <user@localhost>\n')
send_server.recv(4096)
send_server.send(b'RCPT TO: <prokingk@localhost>\n')
send_server.recv(4096)
send_server.send(b'DATA\n')
send_server.recv(4096)
send_server.send(b'Subject: Warning\nTest warning\n.\n')
send_server.recv(4096)
send_server.send(b'QUIT\n')
