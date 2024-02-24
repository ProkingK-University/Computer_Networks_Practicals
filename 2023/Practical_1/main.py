#!/usr/bin/env python3

import random

num1 = random.randint(1, 100)
num2 = random.randint(1, 100)

if num1 > num2:
    larger_num, smaller_num = num1, num2
else:
    larger_num, smaller_num = num2, num1

print ("Content-type: text/html\n");

print ("<html>");
print ("<body>");

print ("<p>Pick the biggest number</p>");

print(f"<a href='../correct.html'>{larger_num}</a>")
print(f"<a href='../wrong.html'>{smaller_num}</a>")

print ("</body>");
print ("</html>");