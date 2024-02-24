import json
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 12345

s.bind(('', port))

s.listen(5)

print('Server is listening')

appointments = []

try:
    with open('appointments.txt', 'r') as f:
        if f.read().strip():
            f.seek(0)
            appointments = json.load(f)
except FileNotFoundError:
    pass

while True:
    c, addr = s.accept()
    print('Got connection from', addr)
    
    while True:
        request = c.recv(1024).decode('utf-8')

        if request.startswith('ADD '):
            appointment = json.loads(request[4:])
            appointments.append(appointment)
            c.send('Appointment added\n'.encode('utf-8'))
        elif request.startswith('GET '):
            index = int(request[4:])
            c.send(json.dumps(appointments[index]).encode('utf-8'))
        elif request.startswith('DELETE '):
            index = int(request[7:])
            del appointments[index]
            c.send('Appointment deleted\n'.encode('utf-8'))

        # Save appointments to file
        with open('appointments.txt', 'w') as f:
            json.dump(appointments, f)