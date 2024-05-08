import re
import socket

pop3_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

pop3_server.connect(('localhost', 110))
pop3_server.recv(4096)
pop3_server.send(b'USER prokingk\n')
pop3_server.recv(4096)
pop3_server.send(b'PASS <password>\n')
pop3_server.recv(4096)
pop3_server.send(b'LIST\n')

response = pop3_server.recv(4096).decode()
email_count = len(response.split('\n')) - 2

for i in range(1, email_count + 1):
    email_data = b''
    pop3_server.send(f'RETR {i}\n'.encode())

    while True:
        data = pop3_server.recv(4096)

        if data.endswith(b'\r\n.\r\n'):
            email_data += data[:-5]
            break

        email_data += data

    email_str = email_data.decode()
    
    subject_match = re.search(r'Subject:\s*(.+)', email_str, re.IGNORECASE)
    subject = subject_match.group(1).strip() if subject_match else 'No Subject'

    print(f'Email {i} Subject: {subject}')
    
    bcc_match = re.search(r'Bcc:\s*(.+)', email_str, re.IGNORECASE)

    if bcc_match:
        bcc_recipients = bcc_match.group(1).split(',')

        if 'prokingk@localhost' in [r.strip() for r in bcc_recipients]:
            smtp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            smtp_server.connect(('localhost', 25))
            smtp_server.recv(4096)
            smtp_server.send(b'HELO localhost\n')
            smtp_server.recv(4096)
            smtp_server.send(b'MAIL FROM: <user@localhost>\n')
            smtp_server.recv(4096)
            smtp_server.send(b'RCPT TO: <prokingk@localhost>\n')
            smtp_server.recv(4096)
            smtp_server.send(b'DATA\n')
            smtp_server.recv(4096)

            warning_message = f'Subject: [BCC Warning] {subject}\n\nYou received a BCC email with the subject: {subject}\n.\n'
            smtp_server.send(warning_message.encode())
            smtp_server.recv(4096)

            smtp_server.send(b'QUIT\n')

            smtp_server.close()

pop3_server.close()
