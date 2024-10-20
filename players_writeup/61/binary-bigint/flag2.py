modN = 69483608101841844910538063317910179071261608947345104326117156072698062071407510513433217022202839062113775686162607830714630035057330712062878972400216838155822694169773732124412390444095656404923563061212422133014831246867026567952553116852379693384751909168419484264325180118579717131699347335537912725051

p = 8335682821571478490352906606412138453297454194998876807433197708759168456488683327650734100655791032147064777500485138827074940225766907860020163251546027

q = 8335682821571478490352906606412138453297454194998876807433197708759168456488683327650734100655791032070103480011988622054095135235550008195677895679112113

assert(p * q == modN)

password = 9017527018249538840933836427690835904014049038300469950152127075415617866384932155389002589266443273376421718270096207566581370751147614415030601174048247023898066098901995596847357482450254374918683501015573127167984706955595132684311411494533906442676952738005821838293318638222403199255205048722982300131

phi = (p - 1) * (q - 1)
e = 65537
d = pow(e, -1, phi)

text = pow(password, d, modN)

s = ""
while text > 0:
    s = s + chr(text % 128)
    text //= 128
print(''.join(list(reversed(s))))