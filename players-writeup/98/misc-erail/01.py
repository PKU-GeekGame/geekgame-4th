import base64


code = "amtj=78e1VY=4CdkNO=77Um5h=58b1d6=70S0hk=6EZlJE=61bkdJ=41U3Z6=6BY30="

output = ""

i = 0
while i < len(code):
  if code[i] == "=" and i + 3 < len(code):
    output += chr(int(code[i + 1 : i + 3], 16))
    i += 3
  else:
    output += base64.b64decode(code[i : i + 4]).decode()
    i += 4

print(output)
