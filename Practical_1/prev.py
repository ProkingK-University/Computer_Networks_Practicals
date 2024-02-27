#!/usr/bin/env python3

with open('numbers.txt', 'r') as file:
    x = int(file.readline().strip())
    y = int(file.readline().strip())
    z = int(file.readline().strip())

end = True if x == 0 and y == 1 and z == 1 else False

if end:
    x = 0
    y = 1
    z = 1
else:
    temp = x
    x = y - x
    z = y
    y = temp

with open('numbers.txt', 'w') as f:
    f.write(str(x) + '\n')
    f.write(str(y) + '\n')
    f.write(str(z) + '\n')

print(
f"""Content-Type: text/html

<html>
<body>
<span>{'---' if end else x}</span>
<span> </span>
<span>{0 if end else y}</span>
<span> </span>
<span>{z}</span>
<br>
<a href="next.py">Next</a>
{'<p href="prev.py">Previous</p>' if end else '<a href="prev.py">Previous</a>'}
</body>
</html>
"""
)