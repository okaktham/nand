// This is a test ASM file for Parser + Code

@2        // A-instruction: symbol = 2
D=A       // C-instruction: dest = D, comp = A
@3        // A-instruction: symbol = 3
D=D+A     // C-instruction: dest = D, comp = D+A
@0        // A-instruction: symbol = 0
M=D       // C-instruction: dest = M, comp = D
0;JMP     // C-instruction: comp = 0, jump = JMP
