import numpy as np
import sympy as sp
import subprocess

def byteArray2BigInt(byteArray):
    ans = 0
    base = 0x80
    for c in byteArray:
        ans = ans * base + c
    return ans

def bigInt2String(bigInt):
    base = 0x80
    ans = ""
    while bigInt > 0:
        ans = chr(bigInt % base) + ans
        bigInt //= base
    return ans

S1_ba = [0x01,0x45,0x72,0x56,0x16,0x46,0x57,0x4a,0x73,0x36,0x51,0x75,0x70,0x04,0x3c,0x7b,0x0f,0x5d,0x28,0x6f,0x0b,0x29,0x73,0x5b,0x10,0x7a,0x7e,0x32,0x5e,0x78,0x3b,0x54,0x32,0x4b,0x08,0x79,0x0a,0x1e,0x5e,0x7a,0x63,0x7d,0x1d,0x5f,0x54,0x7c,0x62,0x4f,0x69,0x01,0x68,0x39,0x39,0x49,0x44,0x3e,0x08,0x51,0x63,0x40,0x6c,0x30,0x4d,0x6c,0x14,0x24,0x7a,0x55,0x41,0x10,0x2d,0x3d,0x6d,0x63,0x64,0x37,0x3b,0x7e,0x0b,0x70,0x7e,0x4d,0x09,0x6d,0x18,0x2d,0x58,0x1e,0x7d,0x3b,0x19,0x1f,0x15,0x13,0x5a,0x73,0x08,0x1f,0x3f,0x12,0x22,0x2e,0x43,0x14,0x24,0x4b,0x35,0x04,0x55,0x5e,0x49,0x7f,0x72,0x69,0x7c,0x11,0x64,0x06,0x64,0x4d,0x48,0x41,0x69,0x7d,0x1a,0x02,0x74,0x43,0x46,0x05,0x44,0x33,0x3c,0x70,0x1e,0x6f,0x2f,0x32,0x4e,0x44,0x61,0x07,0x5f,0x50,0x50,0x7c,0x3b]
S2_ba = [0x19,0x57,0x32,0x3f,0x29,0x7e,0x16,0x10,0x3d,0x18,0x6d,0x26,0x27,0x22,0x6d,0x18,0x4e,0x28,0x29,0x35,0x78,0x74,0x2a,0x4d,0x0b,0x4f,0x36,0x01,0x56,0x67,0x78,0x1b,0x2e,0x6d,0x4e,0x72,0x42,0x2f,0x56,0x27,0x29,0x51,0x36,0x25,0x24,0x7d,0x7d,0x19,0x39,0x68,0x42,0x19,0x1d,0x5f,0x7b,0x08,0x24,0x1f,0x18,0x0f,0x41,0x0b,0x3b,0x65,0x26,0x60,0x49,0x11,0x69,0x55,0x75,0x7b,0x2c,0x08,0x32,0x4b,0x4e,0x34,0x17,0x24,0x26,0x70,0x78,0x64,0x73,0x73,0x5e,0x2e,0x7b,0x61,0x45,0x35,0x52,0x2e,0x2c,0x47,0x05,0x38,0x02,0x33,0x02,0x17,0x0b,0x48,0x43,0x3c,0x1e,0x7b,0x1f,0x21,0x43,0x0b,0x47,0x5d,0x69,0x5f,0x1a,0x57,0x42,0x72,0x49,0x31,0x61,0x70,0x3f,0x46,0x17,0x42,0x3a,0x53,0x47,0x7e,0x0f,0x77,0x55,0x2a,0x47,0x2c,0x22,0x79,0x7d,0x31,0x27,0x77,0x53,0x63]

S1 = byteArray2BigInt(S1_ba)
S2 = byteArray2BigInt(S2_ba)
print(S1)
print(S2)
# exit(0)

# Now we need x**33 === S2 (mod S1)

# methods = "ecm,nonRSA,hart,XYXZ,cube_root,carmichael,pastctfprimes,pisano_period,fibonacci_gcd,lattice,fermat,mersenne_primes,partial_q,compositorial_pm1_gcd,qicheng,z3_solver,binary_polinomial_factoring,wolframalpha,kraitchik,factorial_pm1_gcd,noveltyprimes,system_primes_gcd,boneh_durfee,londahl,primorial_pm1_gcd,factor_2PN,SQUFOF,williams_pp1,fermat_numbers_gcd,classical_shor,mersenne_pm1_gcd,qs,partial_d,pollard_p_1,euler,smallfraction,comfact_cn,ecm2,lehman,factordb,roca,dixon,rapid7primes,wiener,small_crt_exp,siqs,smallq,pollard_rho,lucas_gcd,brent,lehmer,neca,pollard_strassen,highandlowbitsequal,same_n_huge_e,hastads,common_factors,common_modulus_related_message"

# for method in methods.split(","):
#     cmd = "python ./RsaCtfTool/RsaCtfTool.py -n {} -e 65537 --decrypt {} --attack {} --private".format(S1, S2, method)
#     print(cmd)
#     ret = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     print(ret.stdout.decode())
#     print(ret.stderr.decode())

x=95273471635946380012970904528547742000824502992083119979307727474899497479041661
print(bigInt2String(x))