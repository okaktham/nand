// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.
    @SCREEN
    D=A 
    @i
    M=D
(LOOP)
    @KBD
    D=M
    @FILL
    D;JGT
    @SCREEN
    D=D+M
    @CLEAR
    D;JLT
    D=M
    @LOOP
    D;JEQ

(FILL)
    @i
    A=M
    M=-1
    @i
    M=M+1
    D=M
    @KBD
    D=A-D
    @FILL
    D;JGT
    @LOOP
    D;JEQ

(CLEAR)
    @i
    A=M
    M=0
    @i
    M=M+1
    D=M
    @KBD
    D=A-D
    @CLEAR
    D;JGT
    @LOOP
    D;JEQ