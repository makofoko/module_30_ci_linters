result = 0
for n in range(1, 11):
    result += n ** 2

code = """result = 0
for n in range(1, 11):
    result += n ** 2

code = {0}{1}{0}
print(code.format(chr(34), code))
"""

print(code.format(chr(34), code))
