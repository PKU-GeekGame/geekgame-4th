; Some important addr in this run
; $116B subroutine to read input
Init:
    LDA #$00    ; check_dup_input
    STA <$D2
    LDA #$00    ; str_length
    STA <$D0
    LDA #$00    ; status
    STA <$D1
    
    
    LDA #$10    ; flag_mem
    STA <$D4


ReadJoyLoop:
    JSR $116B
    EOR $D2    ; check duplicate
    BEQ ReadJoyLoop
    JSR $116B     ; read again, we believe the next input is still the same
    STA <$D2
    
    TAX
    LDA $D1 ; if status is flag mode, jump directly
    CMP #1
    BEQ DUMP_FLAG_CHAR

    TXA
    CMP #$66    ; check if is flag head
    BNE ReadJoyLoop
    
    INC $D1
    LDY #0

DUMP_FLAG_CHAR:
    CLC
    TXA
    ; get higher hex
    LSR A
    LSR A
    LSR A
    LSR A
    STA $10, Y
    INY
    ; get lower hex
    TXA
    AND #$0F
    STA $10, Y
    INY
    ; check if exit state
    TXA
    CMP #$00
    BNE ReadJoyLoop
    
    STY <$D0

Display:

	LDA #$20	 	; A = 0x20. Let's change the PPU Address to $2000
	STA $2006	; Store 0x20 in the PPU Address. (this changes the high byte)
	LDA #$0	 	; A = 0
	STA $2006	; Store 0x00 in the PPU Address. (this changes the low byte)
    
    LDX #$00    ; change this to change the start address of printing
    LDY #0
    LDA #$24 
    
LoopTop:
    STA $2007
    INY
    
    TYA 
    AND #$40
    BEQ LoopTop

    LDY #0
Loop:	
    ; if not in middle, won't print
    ; check whether in middle of screen
    LDA #$24 
    STA $2007
    INY
    
    TYA
    AND #$1E
    BEQ Loop
    
    
    
PRINT:
    LDA $10, X
	STA $2007 	; Store the target character at the next location on nametable.
    INX
    INY
    
	LDA $10, X
	STA $2007 	; Store the target character at the next location on nametable.
    INX
    INY
    
    TXA
    CMP $D0
    BNE Loop


DEAD:
    CMP #1
    BEQ DEAD
    BNE DEAD

    BRK