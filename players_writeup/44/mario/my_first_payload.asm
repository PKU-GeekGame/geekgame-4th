;.BASE $116B
; identical as https://tasvideos.org/8991S

; ReadController:
; 	LDA #$01
; 	STA $4016	; Strobe the controller
; 	STA <$C0
; 	LSR
; 	STA $4016	; Strobe the controller part 2
; LoopCont:
; 	LDA $4016
; 	LSR
; 	ROL <$C0	; This isn’t the most optimal controller reading routine
; 	BCC	LoopCont ; But it takes up fewer bytes, which is important here.
; 	LDA <$C0
; 	RTS		; This specific part is a subroutine.


;.BASE $1181
Main:
    LDA #$00    ; store 0300 at <$C4 
    STA <$C4
    LDA #$03
    STA <$C5
    LDA #$2F
    STA <$C2

StartInput:
    JSR $116B
    EOR #$2F
    BNE StartInput    ; 2F is start byte
    LDY #$00    ; array index
    LDX #$00    ; clear buffer
StrReadLoop:
    JSR $116B
    EOR $C2    ; check duplicate
    BEQ StrReadLoop
    JSR $116B     ; read again, we believe the next input is still the same
    STA <$C2
    
    TAX         ; start actual read
    AND #$20    
    BNE EndReadLoop ; if 0010, break loop
    TXA
    AND #$0F
    TAX 
SecondReadLoop:
    JSR $116B
    EOR $C2    ; check duplicate
    BEQ SecondReadLoop
    JSR $116B     ; read again, we believe the next input is still the same
    STA <$C2
    
    ASL A
    ASL A
    ASL A
    ASL A
    STX <$C3
    ORA $C3
    STA <$C3
    STA [$C4], Y
    INY
     ;prevent overflow
    BNE EndReadflow
    INC $C5

EndReadflow:
    BEQ StrReadLoop
    BNE StrReadLoop
EndReadLoop:
    JMP [$00C4]
    NOP
