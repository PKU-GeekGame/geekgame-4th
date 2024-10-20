import quopri, base64

a = "amtj=78e1VY=4CdkNu=77Um5h=58T1da=50S0hE=4ERlJE=61bmdp=41c3Z6=6BY30="

for i in range(0, len(a), 7):
	print(str(base64.b64decode(a[i:i+4]),encoding='utf-8'),end='')
	print(str(quopri.decodestring(a[i+4:i+7]),encoding='utf-8'),end='')