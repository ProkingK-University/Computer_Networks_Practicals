import http.server
import socketserver

def get_index_page():
    with open('index.html', 'r') as file:
        html = file.read()
    return html

def next_fibonacci():
    with open('numbers.txt', 'r') as file:
        x = int(file.readline().strip())
        y = int(file.readline().strip())
        z = int(file.readline().strip())

    temp = y
    x = y
    y = z
    z = temp + z

    if x == 0 and y == 0 and z == 0:
        x = 0
        y = 1
        z = 1

    with open('numbers.txt', 'w') as f:
        f.write(str(x) + '\n')
        f.write(str(y) + '\n')
        f.write(str(z) + '\n')

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <title>Document</title>
</head>
<body>
<span>{x}</span>
<span> </span>
<span>{y}</span>
<span> </span>
<span>{z}</span>
<br>
<a href="/next">Next</a>
<a href="/prev">Previous</a>
</body>
</html>
"""
    return html

def prev_fibonacci():
    with open('numbers.txt', 'r') as file:
        x = int(file.readline().strip())
        y = int(file.readline().strip())
        z = int(file.readline().strip())

    end = True if x == 0 and y == 1 and z == 1 else False

    if end:
        x = 0
        y = 0
        z = 0
    else:
        temp = x
        x = y - x
        z = y
        y = temp

    with open('numbers.txt', 'w') as f:
        f.write(str(x) + '\n')
        f.write(str(y) + '\n')
        f.write(str(z) + '\n')

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <title>Document</title>
</head>
<body>
<span>{'---' if end else x}</span>
<span> </span>
<span>{0 if end else y}</span>
<span> </span>
<span>{1 if end else z}</span>
<br>
<a href="/next">Next</a>
{'<span href="/prev">Previous</span>' if end else '<a href="/prev">Previous</a>'}
</body>
</html>
"""
    return html

class FibonacciHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = get_index_page()
            self.wfile.write(bytes(html, 'utf8'))

        elif self.path == '/next':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = next_fibonacci()
            self.wfile.write(bytes(html, 'utf8'))

        elif self.path == '/prev':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = prev_fibonacci()
            self.wfile.write(bytes(html, 'utf8'))
        
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

with socketserver.TCPServer(("", 55555), FibonacciHandler) as httpd:
    print("Serving at port", 55555)
    httpd.serve_forever()
