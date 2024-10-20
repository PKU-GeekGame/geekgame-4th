{https://zhidao.baidu.com/question/143998721.html}
const
    maxlen=1200;
type  
    bigint=object
        n:array[0..maxlen] of longint;
        function add(b:bigint): bigint;
        function sub(b:bigint): bigint;
        function mul(b:Longint): bigint;
        function mul2(b:bigint): bigint;
        function compare(b:bigint): Boolean;
        function modn(b:bigint): bigint;
    end;
function bigint.compare(b:bigint): Boolean;
var
    i: longint;
begin
    if n[0] > b.n[0] then
        exit(True);
    if n[0] < b.n[0] then
        exit(False);
    for i := n[0] downto 1 do
    begin
        if n[i] > b.n[i] then
            exit(True);
        if n[i] < b.n[i] then
            exit(False);
    end;
    exit(True);
end;
function bigint.add(b:bigint): bigint;
var
    i, Len: longint;
begin
    FillChar(add, SizeOf(add), 0); 
    if n[0] > b.n[0] then
    Len := n[0]
    else
    Len := b.n[0];
    for i := 1 to Len do
    begin
        Inc(add.n[i], n[i] + b.n[i]);
        if add.n[i] >= 10 then
        begin
            Dec(add.n[i], 10);
            Inc(add.n[i + 1]);
        end;
    end;
    if add.n[Len + 1] > 0 then
        Inc(Len);
    add.n[0] := Len;
end;
function bigint.sub(b:bigint): bigint;
var
    i, Len: longint;
begin
    FillChar(sub, SizeOf(sub), 0);
    Len := n[0];
    for i := 1 to Len do
    begin
        Inc(sub.n[i], n[i] - b.n[i]);
        if sub.n[i] < 0 then
        begin
            Inc(sub.n[i], 10);
            Dec(sub.n[i + 1]);
        end;
    end;
    while (Len > 1) and (sub.n[Len] = 0) do
        Dec(Len);
    sub.n[0] := Len;
end;
function bigint.mul(b:longint): bigint;
var
    i, Len: longint;
begin
    FillChar(mul, SizeOf(mul), 0);
    Len := n[0];
    for i := 1 to Len do
    begin
        Inc(mul.n[i], n[i] * b);
        Inc(mul.n[i + 1], mul.n[i] div 10);
        mul.n[i] := mul.n[i] mod 10;
    end;
    Inc(Len);
    while (mul.n[Len] >= 10) do
    begin
        mul.n[Len + 1] := mul.n[Len] div 10;
        mul.n[Len] := mul.n[Len] mod 10;
        Inc(Len);
    end;
    while (Len > 1) and (mul.n[Len] = 0) do
    Dec(Len);
    mul.n[0] := Len;
end;
function bigint.mul2(b:bigint): bigint;
var
    i, j, Len: longint;
begin
    FillChar(mul2, SizeOf(mul2), 0);
    for i := 1 to n[0] do
        for j := 1 to b.n[0] do
        begin
            Inc(mul2.n[i + j - 1], n[i] * b.n[j]);
            Inc(mul2.n[i + j], mul2.n[i + j - 1] div 10);
            mul2.n[i + j - 1] := mul2.n[i + j - 1] mod 10;
        end;
    Len := n[0] + b.n[0] + 1;
    while (Len > 1) and (mul2.n[Len] = 0) do
        Dec(Len);
    mul2.n[0] := Len;
end;
function bigint.modn(b:bigint): bigint;
var  
    i, Len: longint;
begin
    FillChar(modn, SizeOf(modn), 0);
    Len := n[0];
    modn.n[0] := 1;
    for i := Len downto 1 do
    begin
        modn:=modn.mul(10);
        modn.n[1] := n[i];
        while (modn.compare(b)) do
        begin
            modn:=modn.sub(b);
        end;
    end;
end;
function createnum(x:longint): bigint;
var
    Len: longint;
begin
    FillChar(createnum, SizeOf(createnum), 0);
    createnum.n[1]:=x;
    Len:=1;
    while (createnum.n[Len] >= 10) do
    begin
        createnum.n[Len + 1] := createnum.n[Len] div 10;
        createnum.n[Len] := createnum.n[Len] mod 10;
        Inc(Len);
    end;
    createnum.n[0]:=Len;
end;
{procedure printnum(x:bigint);
var  
    i: longint;
begin
    for i := x.n[0] downto 1 do
    begin
        write(x.n[i]);
    end;
end;}
function str2int(x:string):bigint;
var  
    i: longint;
begin
    str2int:=createnum(0);
    for i:=1 to length(x) do str2int:=str2int.mul(128).add(createnum(ord(x[i])));
end;
function checkflag1(x:bigint):boolean;
var  
    a, b:bigint;
begin
    a:=x.mul2(x).add(str2int(#101#47#43#15#10#109#35#125#61#117#115#124#32#87#22#51#66#35)).mul2(x);
    b:=x.mul2(x).mul2(str2int(#1#76#12#55#0#9#7#100#32#76)).add(str2int(#16#10#84#42#63#114#12#78#126#73#29#70#100#68#126#49#65#74#14#65#105#60#42#0#41#45#80));
    checkflag1:=a.compare(b) and b.compare(a);
end;
var option:1..4;
    s:string;
    n:longint;
    m,v,k:bigint;
    ok:boolean;
begin
    m:=str2int(#1#69#114#86#22#70#87#74#115#54#81#117#112#4#60#123#15#93#40#111#11#41#115#91#16#122#126#50#94#120#59#84#50#75#8#121#10#30#94#122#99#125#29#95#84#124#98#79#105#1#104#57#57#73#68#62#8#81#99#64#108#48#77#108#20#36#122#85#65#16#45#61#109#99#100#55#59#126#11#112#126#77#9#109#24#45#88#30#125#59#25#31#21#19#90#115#8#31#63#18#34#46#67#20#36#75#53#4#85#94#73#127#114#105#124#17#100#6#100#77#72#65#105#125#26#2#116#67#70#5#68#51#60#112#30#111#47#50#78#68#97#7#95#80#80#124#59);
    v:=str2int(#25#87#50#63#41#126#22#16#61#24#109#38#39#34#109#24#78#40#41#53#120#116#42#77#11#79#54#1#86#103#120#27#46#109#78#114#66#47#86#39#41#81#54#37#36#125#125#25#57#104#66#25#29#95#123#8#36#31#24#15#65#11#59#101#38#96#73#17#105#85#117#123#44#8#50#75#78#52#23#36#38#112#120#100#115#115#94#46#123#97#69#53#82#46#44#71#5#56#2#51#2#23#11#72#67#60#30#123#31#33#67#11#71#93#105#95#26#87#66#114#73#49#97#112#63#70#23#66#58#83#71#126#15#119#85#42#71#44#34#121#125#49#39#119#83#99);
    write('Which flag do you want to check? (1 or 2) ');
    readln(option);
    write('Flag: ');
    readln(s);
    k:=str2int(s);
    Case option of
        1: begin
            n:=length(s) div 3;
            ok:=checkflag1(str2int(copy(s,1,n))) and checkflag1(str2int(copy(s,1+n,n))) and checkflag1(str2int(copy(s,1+2*n)));
        end;
        2: begin
            for n:=1 to 16 do k:=k.mul2(k).modn(m);
            k:=k.mul2(str2int(s)).modn(m);
            ok:=k.compare(v) and v.compare(k);
        end;
    else
        WriteLn ('Invalid option');
        halt;
    end;
    if ok then writeln('Correct') else writeln('Wrong');
end. 