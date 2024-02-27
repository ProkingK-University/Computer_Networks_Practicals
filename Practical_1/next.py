#!/usr/bin/env python3

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

print(
f"""Content-Type: text/html

<html>
<body>
<span>{x}</span>
<span> </span>
<span>{y}</span>
<span> </span>
<span>{z}</span>
<br>
<a href="next.py">Next</a>
<a href="prev.py">Previous</a>
</body>
</html>
"""
)