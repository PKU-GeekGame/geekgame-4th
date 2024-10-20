from pwn import *
conn=remote("geekgame-prob",10017)
conn.sendline("7:MEUCIGxPGbImn6azAJ4z52JihiU4oOwzaLnIoTkQGAtpcD-pAiEA4DDj2GDZze6e-Egafn5LkCZrWjXV1OyrvlW_rCNuLxE=")
conn.sendline("\n"*10000)
nums=[]
for i in range(10000):
    nums.append(int(conn.recvline().decode().replace("Please input your token:","")))
    
... # period=53

import sympy
sym=[sympy.symbols(f"x{i}") for i in range(53)]
eqs=[sym[(607+k-273)%53]+sym[(607+k-607)%53]-sym[(607+k)%53]-max([(nums[i-273]+nums[i-607]-nums[i]+512)%2**32-512 for i in range(607+k,10000,53)]) for k in range(53)]
eqs_sol=sympy.solve(eqs)
print(bytes([eqs_sol[i] for i in sym]))