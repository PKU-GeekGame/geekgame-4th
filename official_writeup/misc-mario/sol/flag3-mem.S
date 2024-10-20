; NES memory dump for printing controller input to screen in Super Mario Bros. ACE.
; Written by MaxXing, 2024-10.
;
; This file can be assembled by `asm6f`.

USER_INPUT    = $0000
NT_OFFSET     = $0001
NT_OFFSET_HI  = $0002

PPU_CTRL      = $2000
PPU_STATUS    = $2002
PPU_SCROLL    = $2005
PPU_ADDR      = $2006
PPU_DATA      = $2007

CONTROLLER1   = $4016

; ============================================================
; Memory that will be initialized by Super Mario Bros.
; ============================================================
  .org  $0000
  .pad  $0160, $ff

; ============================================================
; Start of the uninitialized RAM.
; ============================================================
  .org  $0160

  ; Nothing yet.

; ============================================================
; Entry of ACE.
; ============================================================
  .org  $0181

  lda #%00010000      ; Reset PPU status.
  sta PPU_CTRL
  lda #$20            ; Set nametable offset to the corner of screen.
  sta NT_OFFSET
  lda #$00
  sta NT_OFFSET_HI

DrawFrame:            ; Draw the current frame.
  lda PPU_STATUS      ; Wait for next frame.
  bpl DrawFrame

  lda #$01            ; Strobe controller.
  sta CONTROLLER1
  lda #$80            ; Initialize user input and strobe again.
  sta USER_INPUT
  sta CONTROLLER1
ReadLoop:             ; Read input.
  lda CONTROLLER1     ; Read controller to carry bit.
  lsr a
  ror USER_INPUT      ; Shift into USER_INPUT.
  bcc ReadLoop
  ldx USER_INPUT      ; Skip if no input.
  beq DrawFrame

  lda #$20            ; Set PPU address to nametable.
  ora NT_OFFSET_HI
  sta PPU_ADDR
  lda NT_OFFSET
  sta PPU_ADDR

  txa                 ; Write user input to nametable.
  lsr a
  lsr a
  lsr a
  lsr a
  sta PPU_DATA
  txa
  and #$0f
  sta PPU_DATA

  lda NT_OFFSET       ; Update offset.
  clc
  adc #2
  sta NT_OFFSET
  lda NT_OFFSET_HI
  adc #0
  sta NT_OFFSET_HI

  lda #$00            ; Reset scroll.
  sta PPU_SCROLL
  sta PPU_SCROLL

  jmp DrawFrame       ; Loop forever.

; ============================================================
; Rest of memory.
; ============================================================
  .org  $01ea
  .pad  $07d7, $ff

  .org  $07d7
  .db   $00, $00, $00  ; High score.
  .db   $00, $00, $00
  .pad  $07fd, $ff

  .org  $07fd
  .db   $16            ; Last played world.
  .pad  $07ff, $ff

  .org  $07ff
  .db   $a5            ; Magic number, will be checked by the game.
