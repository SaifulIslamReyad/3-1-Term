;*****************************************
;     MDA-Win8086 EXPERIMENT PROGRAM    *
;     FILENAME  : FND.ASM
;     PROCESSOR : I8086
;     FUNCTION  : 7-Segment Control via 8255
;*****************************************
CODE SEGMENT
ASSUME CS:CODE,DS:CODE,ES:CODE,SS:CODE

; 8255 PORT ADDRESSES
PPIC_C  EQU 1FH
PPIC    EQU 1DH
PPIB    EQU 1BH
PPIA    EQU 19H

ORG 1000H

; Initialize 8255 in Mode 0
START:
    MOV AL,10000000B   ; Set Control Word
    OUT PPIC_C,AL
    MOV AL,11110000B   ; Output config for Port B
    OUT PPIB,AL
    MOV AL,00000000B   ; All output mode
    OUT PPIC,AL

; --- CALL ANY ONE FUNCTION HERE ---
    CALL DISPLAY_9_TO_0
;   CALL DISPLAY_0_TO_9
;   CALL DISPLAY_EVEN
;   CALL DISPLAY_ODD

INT 3 ; Stop Execution

; -------------------------------
; Display Digits from 9 to 0
; -------------------------------
DISPLAY_9_TO_0:
    MOV SI, OFFSET DIGIT_9_TO_0
DISPLAY_LOOP1:
    MOV AL, BYTE PTR [SI]
    CMP AL, 0FFH
    JE RETURN
    OUT PPIA, AL
    CALL TIMER
    INC SI
    JMP DISPLAY_LOOP1

; -------------------------------
; Display Digits from 0 to 9
; -------------------------------
DISPLAY_0_TO_9:
    MOV SI, OFFSET DIGIT_0_TO_9
DISPLAY_LOOP2:
    MOV AL, BYTE PTR [SI]
    CMP AL, 0FFH
    JE RETURN
    OUT PPIA, AL
    CALL TIMER
    INC SI
    JMP DISPLAY_LOOP2

; -------------------------------
; Display Even Digits: 0, 2, 4, 6, 8
; -------------------------------
DISPLAY_EVEN:
    MOV SI, OFFSET DIGIT_EVEN
DISPLAY_LOOP3:
    MOV AL, BYTE PTR [SI]
    CMP AL, 0FFH
    JE RETURN
    OUT PPIA, AL
    CALL TIMER
    INC SI
    JMP DISPLAY_LOOP3

; -------------------------------
; Display Odd Digits: 1, 3, 5, 7, 9
; -------------------------------
DISPLAY_ODD:
    MOV SI, OFFSET DIGIT_ODD
DISPLAY_LOOP4:
    MOV AL, BYTE PTR [SI]
    CMP AL, 0FFH
    JE RETURN
    OUT PPIA, AL
    CALL TIMER
    INC SI
    JMP DISPLAY_LOOP4

; -------------------------------
; Delay Function
; -------------------------------
TIMER:
    MOV CX, 5000
TIMER1:
    NOP
    NOP
    NOP
    NOP
    LOOP TIMER1
    RET

; -------------------------------
; Return to Main Program
; -------------------------------
RETURN:
    RET

; -------------------------------
; Segment Code for Digits
; -------------------------------
; Common-Cathode 7-segment encoding
DIGIT_0_TO_9:
    DB 11000000B ; 0
    DB 11111001B ; 1
    DB 10100100B ; 2
    DB 10110000B ; 3
    DB 10011001B ; 4
    DB 10010010B ; 5
    DB 10000010B ; 6
    DB 11111000B ; 7
    DB 10000000B ; 8
    DB 10010000B ; 9
    DB 0FFH       ; End

DIGIT_9_TO_0:
    DB 10010000B ; 9
    DB 10000000B ; 8
    DB 11111000B ; 7
    DB 10000010B ; 6
    DB 10010010B ; 5
    DB 10011001B ; 4
    DB 10110000B ; 3
    DB 10100100B ; 2
    DB 11111001B ; 1
    DB 11000000B ; 0
    DB 0FFH       ; End

DIGIT_EVEN:
    DB 11000000B ; 0
    DB 10100100B ; 2
    DB 10011001B ; 4
    DB 10000010B ; 6
    DB 10000000B ; 8
    DB 0FFH       ; End

DIGIT_ODD:
    DB 11111001B ; 1
    DB 10110000B ; 3
    DB 10010010B ; 5
    DB 11111000B ; 7
    DB 10010000B ; 9
    DB 0FFH       ; End

CODE ENDS
END
