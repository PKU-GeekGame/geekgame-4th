; Written in $0181; safe zone $0160 to $01E4
	LDA #$08
	STA $2001    ; disable rendering sprite
    LDY #$00     ; counter; write <= EE chars
VBLoop:
    JSR $016B    ; read controller
    CMP $1F0
    BNE Pause    ; must be a new frame, wait for a while
Pause:
    LDA $2002	 ; Wait for Vblank
	BPL VBLoop	 ; Loop
	JSR $016B    ; read controller (guarantee new input being read)
    
    STA $1F0
    LDA #$01
RevLoop:
    LSR $1F0     ; extract the lowest bit...
    ROL A        ; ...send it to the lowest bit of A
    BCC RevLoop  ; repeat 8 times
    TAX          ; save the correct byte to X
    
    LDA #$21
    STA $2006    ; write draw position 1st byte
    TYA
    AND #$0F
    CMP #$02
    BCS WriteOK  ; branch if lo half byte of A >= 2
    INY
    INY          ; skip these positions where lo half byte of A < 2
WriteOK:
    STY $2006    ; write draw position 2nd byte
    LDA #$10
	STA $2000    ; address inc mode; NMI off
	LDA #$00
	STA $2005
	STA $2005    ; disable scroll
    
    TXA
    AND #$F0
    LSR
    LSR
    LSR
    LSR
    STA $2007    ; first half byte
    TXA
    AND #$0F
    STA $2007    ; next half byte
    STX $1F0
    INY
    INY
    BPL VBLoop   ; to a new frame
NOPLoop:
    LDA #$00
    BEQ NOPLoop
.END
