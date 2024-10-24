l1 = [0x01, 0x45, 0x72, 0x56, 0x16, 0x46, 0x57, 0x4A, 0x73, 0x36, 0x51, 0x75, 0x70, 0x04, 0x3C, 0x7B, 0x0F, 0x5D, 0x28, 0x6F, 0x0B, 0x29, 0x73, 0x5B, 0x10, 0x7A, 0x7E, 0x32, 0x5E, 0x78, 0x3B, 0x54, 0x32, 0x4B, 0x08, 0x79, 0x0A, 0x1E, 0x5E, 0x7A, 0x63, 0x7D, 0x1D, 0x5F, 0x54, 0x7C, 0x62, 0x4F, 0x69, 0x01, 0x68, 0x39, 0x39, 0x49, 0x44, 0x3E, 0x08, 0x51, 0x63, 0x40, 0x6C, 0x30, 0x4D, 0x6C, 0x14, 0x24, 0x7A, 0x55, 0x41, 0x10, 0x2D, 0x3D, 0x6D, 0x63, 0x64, 0x37, 0x3B, 0x7E, 0x0B, 0x70, 0x7E, 0x4D, 0x09, 0x6D, 0x18, 0x2D, 0x58, 0x1E, 0x7D, 0x3B, 0x19, 0x1F, 0x15, 0x13, 0x5A, 0x73, 0x08, 0x1F, 0x3F, 0x12, 0x22, 0x2E, 0x43, 0x14, 0x24, 0x4B, 0x35, 0x04, 0x55, 0x5E, 0x49, 0x7F, 0x72, 0x69, 0x7C, 0x11, 0x64, 0x06, 0x64, 0x4D, 0x48, 0x41, 0x69, 0x7D, 0x1A, 0x02, 0x74, 0x43, 0x46, 0x05, 0x44, 0x33, 0x3C, 0x70, 0x1E, 0x6F, 0x2F, 0x32, 0x4E, 0x44, 0x61, 0x07, 0x5F, 0x50, 0x50, 0x7C, 0x3B]
l2 = [0x19, 0x57, 0x32, 0x3F, 0x29, 0x7E, 0x16, 0x10, 0x3D, 0x18, 0x6D, 0x26, 0x27, 0x22, 0x6D, 0x18, 0x4E, 0x28, 0x29, 0x35, 0x78, 0x74, 0x2A, 0x4D, 0x0B, 0x4F, 0x36, 0x01, 0x56, 0x67, 0x78, 0x1B, 0x2E, 0x6D, 0x4E, 0x72, 0x42, 0x2F, 0x56, 0x27, 0x29, 0x51, 0x36, 0x25, 0x24, 0x7D, 0x7D, 0x19, 0x39, 0x68, 0x42, 0x19, 0x1D, 0x5F, 0x7B, 0x08, 0x24, 0x1F, 0x18, 0x0F, 0x41, 0x0B, 0x3B, 0x65, 0x26, 0x60, 0x49, 0x11, 0x69, 0x55, 0x75, 0x7B, 0x2C, 0x08, 0x32, 0x4B, 0x4E, 0x34, 0x17, 0x24, 0x26, 0x70, 0x78, 0x64, 0x73, 0x73, 0x5E, 0x2E, 0x7B, 0x61, 0x45, 0x35, 0x52, 0x2E, 0x2C, 0x47, 0x05, 0x38, 0x02, 0x33, 0x02, 0x17, 0x0B, 0x48, 0x43, 0x3C, 0x1E, 0x7B, 0x1F, 0x21, 0x43, 0x0B, 0x47, 0x5D, 0x69, 0x5F, 0x1A, 0x57, 0x42, 0x72, 0x49, 0x31, 0x61, 0x70, 0x3F, 0x46, 0x17, 0x42, 0x3A, 0x53, 0x47, 0x7E, 0x0F, 0x77, 0x55, 0x2A, 0x47, 0x2C, 0x22, 0x79, 0x7D, 0x31, 0x27, 0x77, 0x53, 0x63]


def enc(l):
    res = 0
    for i in range(len(l)):
        res = res * 128 + l[i]
    return res

def dec(x):
    res = []
    while x > 0:
        res = [x % 128] + res
        x = x // 128
    return bytes(res)

N = enc(l1)
y = enc(l2)
e = 65537
p = 8335682821571478490352906606412138453297454194998876807433197708759168456488683327650734100655791032070103480011988622054095135235550008195677895679112113
q = 8335682821571478490352906606412138453297454194998876807433197708759168456488683327650734100655791032147064777500485138827074940225766907860020163251546027

assert N == p * q

# decrypt x such that x^e = y mod N

phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)
x = pow(y, d, N)
print(dec(x))
