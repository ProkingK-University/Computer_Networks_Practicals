import random
import http.server
import socketserver
from urllib.parse import parse_qs

def get_index_page():
    with open('index.html', 'r') as file:
        html = file.read()
    return html

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

class QuestionHandler(http.server.SimpleHTTPRequestHandler):
    questions = parse_questions("questions.txt")
    current_question = random.choice(questions)

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = get_index_page()
            self.wfile.write(bytes(html, 'utf8'))

        elif self.path == '/question':
            QuestionHandler.current_question = random.choice(QuestionHandler.questions)
            self.send_response(200)
            self.end_headers()
            content = self.get_question_content(QuestionHandler.current_question)
            self.wfile.write(content.encode('utf-8'))

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        user_answer = int(parse_qs(post_data.decode())['answer'][0])

        if user_answer in QuestionHandler.current_question['correct']:
            response = "<p>Congratulations! That's the correct answer.</p>"
        else:
            correct_answers = ', '.join([str(i) for i in QuestionHandler.current_question['correct']])
            response = f"<p>Sorry, that's not correct. The correct answer was: {correct_answers}.</p>"

        response += "<p>Would you like to <a href='/question'>play again</a>?</p>"

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))

    def get_question_content(self, question):
        content = f"<html><body><h1>{question['question']}</h1><form method='POST'>"

        for i, answer in enumerate(question['answers']):
            content += f"<input type='radio' name='answer' value='{i}'>{chr(65+i)}. {answer}<br>"

        content += "<input type='submit' value='Submit'></form></body></html>"

        return content

with socketserver.TCPServer(("", 55555), QuestionHandler) as httpd:
    print("Serving at port", 55555)
    httpd.serve_forever()
