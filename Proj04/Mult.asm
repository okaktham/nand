// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Minimal direct decrement loop    
    @2
    M=0 // R2 = 0
    @0  // loading R0
    D=M
    @END
    D;JEQ // terminate if R0 == 0
    @1
    D=M
    @END
    D;JEQ // terminate if R1 == 0

(LOOP)
    @1 // terminate if R1 == 0
    D=M
    @END
    D;JEQ
    @0
    D=M
    @2
    M=D+M // Add R0 to R2 -> R2
    @1
    M=M-1
    @LOOP
    0;JMP // Loop back until R1 is 0
(END)
    @END
    0;JMP