// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

// Put your code here.
    @24576
    D=A
    @screen_end
    M=D


(LOOP)
    @SCREEN
    D=A
    @addr
    M=D

    @color
    M=0

    @KBD
    D=M
    @PRESSED
    D;JNE // if D != 0, set color to -1
    @UPDATE_SCREEN
    0;JMP


(PRESSED)
    @color
    M=-1

(UPDATE_SCREEN)
    @addr
    D=M
    @screen_end
    D=M-D

    @LOOP
    D;JEQ

    @color
    D=M
    @addr
    A=M
    M=D
    @addr
    M=M+1

    @UPDATE_SCREEN
    0;JMP