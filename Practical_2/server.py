import socket
import random
import threading

def parse_questions(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()

    questions = []
    question = {'question': '', 'answers': [], 'correct': []}

    for line in lines:
        if line.startswith('?'):
            question = {'question': line[1:].strip(), 'answers': [], 'correct': []}
        elif line.startswith('-'):
            question['answers'].append(line[1:].strip())
        elif line.startswith('+'):
            question['answers'].append(line[1:].strip())
            question['correct'].append(len(question['answers']) - 1)
        elif line.strip() == '':
            if len(question['correct']) == 0:
                question['answers'].append('None of the above')
                question['correct'] = [len(question['answers']) - 1]
            elif len(question['correct']) > 1:
                question['answers'].append('More than one of the above')
                question['correct'] = [len(question['answers']) - 1]

            questions.append(question)

    return questions

def handle_client(conn, addr, questions):
    print('Connected by', addr)

    while True:

        conn.sendall(b'\033[2J')

        conn.sendall(f'\033[1;1H'.encode())

        print(questions)

        question = random.choice(questions)
        conn.sendall((question['question'] + '\n').encode())

        for i, answer in enumerate(question['answers']):
            conn.sendall((chr(65+i) + '. ' + answer + '\n').encode())

        data = conn.recv(1024)

        if not data:
            break

        answer = data.decode().strip()

        if ord(answer.upper()) - 65 in question['correct']:
            conn.sendall(b'Congratulations! You are correct.\n')
        else:
            conn.sendall(('The correct answer is ' + ', '.join([chr(65+i) for i in question['correct']]) + '\n').encode())

        conn.sendall(b'Would you like to answer another question? (Y/N)\n')

        data = conn.recv(1024)

        if not data or data.decode().strip().upper() != 'Y':
            break

        conn.close()


def start_server(questions, host='localhost', port=55555):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()

        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr, questions))
            client_thread.start()

questions = parse_questions('questions.txt')
start_server(questions)