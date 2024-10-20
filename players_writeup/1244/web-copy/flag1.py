import re

def subst(s):
    return 'value="' + re.sub(r"<div .+?>|</div>", "", s) + '"'

# Paste the <div> here
print(subst("""
<div class="centralNoiseContent" id="centralNoiseContent1" style="opacity: initial;"><div class="noiseLine">1IO1)(Jl!iI1(1I1O0OOl)(!i|J1iOili!I|l0!|</div><div class="noiseLine">!|1OI))|!1lO|0l(ll(iO!l0((0)|)J)O!JiOiOO</div><div class="noiseLine">|!|!|iJ|J!Il00O|lJ(ii0!OO(lO0)1l1J(!iI||</div><div class="noiseLine">1l!Ii)0l(OIl|I!)|)i11O0lIi1|(0IJ|i00l|Ji</div><div class="noiseLine">0lJJ0J01(1O(OI!i((|1IO(i01OJ!!l)Oli!O|(I</div><div class="noiseLine">I1!0i|(O(iJ00O!ilIO(l|J))Illl(!(i1il(JlI</div></div>
"""))
