from pwn import *
conn=remote("geekgame-prob",10016)
conn.sendline("7:MEUCIGxPGbImn6azAJ4z52JihiU4oOwzaLnIoTkQGAtpcD-pAiEA4DDj2GDZze6e-Egafn5LkCZrWjXV1OyrvlW_rCNuLxE=")
conn.sendline("\n"*10000)
nums=[]
for i in range(10000):
    nums.append(int(conn.recvline().decode().replace("Please input your token:","")))

def tempering(y):
    y ^= (y >> 11)
    y ^= (y <<  7) & 0x9d2c5680
    y ^= (y << 15) & 0xefc60000
    y ^= (y >> 18)
    return y

def untempering(y):
    y ^= (y >> 18)
    y ^= (y << 15) & 0xefc60000
    y ^= ((y <<  7) & 0x9d2c5680) ^ ((y << 14) & 0x94284000) ^ ((y << 21) & 0x14200000) ^ ((y << 28) & 0x10000000)
    y ^= (y >> 11) ^ (y >> 22)
    return y

def generate(v_623,v_227):
    y1 = 0x80000000 | (v_623 & 0x7fffffff)
    z1 = v_227 ^ (y1 >> 1) ^ [0x0, 0x9908b0df][y1 & 0x1]
    y2 = (v_623 & 0x7fffffff)
    z2 = v_227 ^ (y2 >> 1) ^ [0x0, 0x9908b0df][y2 & 0x1]
    return z1,z2

def em(z623,z227,z):
    ans=[]
    for i in range(128):
        for j in range(128):
            for k in range(128):
                v=untempering(z-i)
                v227=untempering(z227-j)
                v623=untempering(z623-k)
                if v in generate(v623,v227):
                    return k

for k in range(60):
    print(em(nums[623+k-623],nums[623+k-227],nums[623+k]))