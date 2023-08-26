// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

// Intialize i to 1 and R2 to 0. R2 will hold the product.
    @i
    M=1

    @R2
    M=0

(LOOP)
    @i
    D=M
    @R0
    D=D-M
    @STOP
    D;JGT
    // product = product + R1
    @R2
    D=M
    @R1
    D=D+M
    @R2
    M=D
    // i = i + 1
    @i
    M=M+1
    // goto LOOP
    @LOOP
    0;JMP

(STOP)
    // R2 = product
    @i
    M=0

(END)
    @END
    0;JMP
