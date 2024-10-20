
import gzip
from pwn import *
import random
from itertools import combinations


def average_bit_count(s):
    return sum(c.bit_count() for c in s) / len(s)

CHARSET = [b ^ 22 for b in range(0x20, 0x7f)]
print(len(CHARSET))
print([p8(c) for c in CHARSET] * 10)

TARGET = b'[What can I say? Mamba out! --KobeBryant]'



def downhill_flag1(score_f = average_bit_count, init:bytes = None, max_t = 100000):
    if init is None:
        to_enc = [p8(c) for c in CHARSET] * 10
        random.shuffle(to_enc)
        to_enc = b''.join(to_enc)
    else:
        to_enc = init

    # mid result
    to_enc_arr = bytearray(to_enc)
    score = 1e20

    swap_comb = list(combinations(range(len(to_enc_arr)), 2))

    for i_step in range(max_t):
        
        ix, iy = random.choice(swap_comb)
        to_enc_arr[ix], to_enc_arr[iy] = to_enc_arr[iy], to_enc_arr[ix]

        # do a loop
        enc_s = gzip.compress(bytes(to_enc_arr))
        prefix = (enc_s + b'\xFF'*256)[:256]
        new_score = score_f(prefix)

        if new_score > score:
            # swap back
            to_enc_arr[ix], to_enc_arr[iy] = to_enc_arr[iy], to_enc_arr[ix]
        else:
            # update score
            score = new_score

        if i_step % 1000 == 0:
            print(i_step, score_f(enc_s[:256]))

    return bytes(to_enc_arr)


GOOD_DOWN_HILL = b'm!$fJW(PDR,1VDQR%PfJ\',#mDS!,$BRf% &+Q&SWB1\'((";8,D/R!;#"V"W#8;&..;*& V"!<99\' .UP;(:&fR) KYD,1 $QQ*%9$8P%1S\',]""W(%#Pf: 1(& 8DJS<&W%6.D8$m98.f0$;;1%$&])9DJ0!V8DP!%P&8S*S"QSJP""!#.B8R#(#$S.1#%J**,9>Y%#R*!BJ9;J;fm.91*fS!+8(P JY/Q3>#&(f.f9($WRD/*)W1 W;*1 *QR"$,PU>R,:!QW9.Q6v4@xxu75onwp\x7f6NEh\x7fx-|lk?\x7fw5hYl-UeL2LG+l+JF`L<?XNv\'EOA]GlY64IsgT|mjK35ac?a~VXAs7kGhxILM>mVe~|kzt@]l+A5[]rpk7-@[uKU2~dK^dg\x7f))r^0?TadI2p{@j/`U\'3jA-gw0<Yb?/NIXhz3O_L}60)>o=lLoKE-=]X/Tv)Gz~ZYm]3ZI[-5sIyj6Q-=FESa4)NIHysAnTZK44|qM:}nxG4CwTz3:l>0`ty<C2G\\ksKd\\4O:o[Tgp?CqN>CeBggUGkH^_yr{yxC=Tp>Eg5k[3}+2\'rgr<rhFC<7rc6aF\\\x7f6qh5yjZ^<oO</|}jhNq}to?shqk]]CdzeFMw@V<Mb0GV{Outt{Fj>3zA3|X-upT`[uO5e@+\x7fx4sEcMvud}?~~F4o_ZBBA]lGnw?K~rE@pO0\\n\\n^s~_0Zep`O22gEtbNHw_I3Fuz=U\\^bcn?}/o7qX_ynHau|=jHtALIIXvoH~`L)szF+Ay7:c}poAv=M:\\pV:{@H2^\\5}ZdVwC@6K\'_aqx[{U7`{,^-CZnw/k@>{-w0cbtY_Y4tgMM|a2F7ZjNcqz`N|=_UmcX\\\x7fcezx=+X\'qbmjhsvly7Gh_bBa\'E5C:vEMrXeL[ZBu`v~YbcN\\Teae^[{r\x7f\x7f{Kt+u|nmHHWx6)O=d[U/bdBTOq\x7fdv^L7M`}blHky2'


def rev_final(GOOD_DOWN_HILL):
    random.seed('Genshin')
    I_SHUF = list(range(len(GOOD_DOWN_HILL)))
    random.shuffle(I_SHUF)
    I_SHUF_REV = [I_SHUF.index(i) for i in range(len(GOOD_DOWN_HILL))]

    orig_input = ''.join([chr(GOOD_DOWN_HILL[I_SHUF_REV[i]] ^ 22) for i, c in enumerate(GOOD_DOWN_HILL)])

    random.seed()

    return (orig_input)

print(rev_final(GOOD_DOWN_HILL))
# flag{ConGraTs-YOUr-pAYlOaD-BeATs-shannon}

def check_mamba(s):
    score = len(TARGET)
    for i in range(len(TARGET)):
        if TARGET[:i+1] in s:
            score -= 1
        else:
            break
    return score



try:
    with open('mamba.tmp', 'rb') as fp:
        opt = fp.read()
except:
    opt = None

opt = downhill_flag1(score_f=check_mamba, init=opt, max_t = 1000000)
print(opt)
print(gzip.compress(opt))

with open('mamba.tmp', 'wb') as fp:
    fp.write(opt)


MAMBA_OUT = rev_final(b'W=Eu,\\$#l9?.D8ZW*>y8DlJ5<`"78Zy+\x7f E:\\n<~`|z:wjQ!A_32L]R_MLU~aH*4%\x7fIgy<?s_osQwPV&Hnm|3,^W6PnY&DV{Y1ht"^fL"f^gd"QN;4\'SlU;gNbg5\' 7hLcN#Q`hhcF5=9QqKN]fMqS(|B)sgO=)T41B5Af 5Ey+j@S+Cuxm+5zP#z;BRf+pA!7\'}Fq\x7f~F4!GYqU+RnK{WoBZ>1Dd%}3},<@6q-@jB/AXmE>r;\'%g[*7qLd2HEAcX7Z>?3dR3SRT.O.eE>p{Y1-&K.s[^K$_@&Qe!M!L%TK9p)}C# |R{"#`uO?udCqGyjIJCyk\x7fGv,]ywy(M5t%ObxS"4~Fcj4~\'oL2st0G, ?;CWx]nYankt$OdR`k\x7fAoYrb;a oHu[Bl9h@HYEjOvJI>MZ*322#88Is60[Vc(mjh:b6]9jf,6kpJMPvG\\NfA):<!hlg\'K24.rkIT:|\\VFK5Vh{uf"aGe[9C8NdH7-%cKSJ;?\\1o<oUI3D".|r]c]$@_{dTQ&mZv/;|X$7^F_1bC\x7f<Xtk8Pl*vW_:0\'4k=2b,N&z,9$_~![qKGt==-<^2!tOZ=eU)`Gw\x7fdlso80pgQtw@buT|-_dl6FE%wR6\\3]r{F%Px$sPI]^ezo8~jwk@0Akn(@eDlbzx~xzpnmI?`?chb/D0,?oPy).w/DX&mnrTh YmUX\\!+L6v&$p#^3{x{Z*|BYvGv =atq6\'Uv>A5{(kcaX6c@q /WPT}z=0%MJvO(s<\\C0uB?-}(I!T*)fVR/V">OJDEn[//a}+S1e1SDY\x7fa(-HOXX\'w:/\x7f.8$J).(*Rg3$wIU[7V_lBN\\^tF-r~&;W]4Vue,1z#pA`;+X*7Je:C#y1E|Ha2mZU[<04f#9rH[M}jpC\\(+2-%xWNZFr:bg7=zQ"MT& H`Br`\x7fU0NxJ*)aeu~.}mP/Ksp9M:>5V\'}xLGQ>WS)S-L9^')

print(MAMBA_OUT)
# flag{the-WhEels-tHAt-SINg-AN-UneNding-DrEAm}