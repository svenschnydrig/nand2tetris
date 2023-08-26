import sys

C_COMMAND_INIT_BITS = '111'

DEST_MNEMONIC_TO_BITS = {
        None : '000',
        'M'  : '001',
        'D'  : '010',
        'MD' : '011',
        'A'  : '100',
        'AM' : '101',
        'AD' : '110',
        'AMD': '111'
    }

COMP_MNEMONIC_TO_BITS = {
        None : '',
        '0'  : '0101010',
        '1'  : '0111111',
        '-1' : '0111010',
        'D'  : '0001100',
        'A'  : '0110000',
        'M'  : '1110000',
        '!D' : '0001101',
        '!A' : '0110001',
        '!M' : '1110001',
        '-D' : '0001111',
        '-A' : '0110011',
        '-M' : '1110011',
        'D+1': '0011111',
        'A+1': '0110111',
        'M+1': '1110111',
        'D-1': '0001110',
        'A-1': '0110010',
        'M-1': '1110010',
        'D+A': '0000010',
        'D+M': '1000010',
        'D-A': '0010011',
        'D-M': '1010011',
        'A-D': '0000111',
        'M-D': '1000111',
        'D&A': '0000000',
        'D&M': '1000000',
        'D|A': '0010101',
        'D|M': '1010101'
    }

JUMP_MNEMONIC_TO_BITS = {
        None : '000',
        'JGT': '001',
        'JEQ': '010',
        'JGE': '011',
        'JLT': '100',
        'JNE': '101',
        'JLE': '110',
        'JMP': '111'
    }

PREDEFINED_SYMBOLS = {
        'SP'  : 0,
        'LCL' : 1,
        'ARG' : 2,
        'THIS': 3,
        'THAT': 4,
        'R0'  : 0,
        'R1'  : 1,
        'R2'  : 2,
        'R3'  : 3,
        'R4'  : 4,
        'R5'  : 5,
        'R6'  : 6,
        'R7'  : 7,
        'R8'  : 8,
        'R9'  : 9,
        'R10' : 10,
        'R11' : 11,
        'R12' : 12,
        'R13' : 13,
        'R14' : 14,
        'R15' : 15,
        'SCREEN': 16384,
        'KBD'   : 24576
    }

def main(): #initializes the I/O files and drives the process
    # Check if a command-line argument was provided
    if len(sys.argv) < 2:
        print("Please provide the .asm filename as a command-line argument.")
        sys.exit(1)

    filename = sys.argv[1]

    # first pass
    lines = []
    counter = 0
    # Open the .asm file in read mode
    with open(filename, 'r') as file:
        for line in file:
            # Process each line here
            line = line.strip().replace(" ", "")
            # Remove content after // 
            line = line.split("//")[0]
            # get whether it's an A-Command, C-Command or Label
            if line:
                if line[0] == '@':
                    counter += 1
                elif line[0] == '(':
                    line = line.replace('(', '').replace(')', '')
                    PREDEFINED_SYMBOLS[line] = counter #+ 1
                else:
                    counter += 1

    # second pass
    lines = []
    counter = 0
    address = 16

    # Open the .asm file in read mode
    with open(filename, 'r') as file:
        for line in file:
            # Process each line here
            line = line.strip().replace(" ", "")
            # Remove content after // 
            line = line.split("//")[0]
            # get whether it's an A-Command, C-Command or Label
            if line:
                if line[0] == '@':
                    if not(line[1].isdigit()):
                        line = line.replace('@', '')
                        if line not in PREDEFINED_SYMBOLS:
                            PREDEFINED_SYMBOLS[line] = address
                            address += 1
                        line = PREDEFINED_SYMBOLS[line]

    lines = []
    counter = 0
    # Open the .asm file in read mode
    with open(filename, 'r') as file:
        for line in file:
            # Process each line here
            line = line.strip().replace(" ", "")
            # Remove content after // 
            line = line.split("//")[0]
            # get whether it's an A-Command, C-Command or Label
            
            if line:
                if line[0] == '(':
                    continue
                if line[0] == '@':
                    line = line.replace('@', '')
                    if not (line[0].isdigit()):
                        if line not in PREDEFINED_SYMBOLS:
                            PREDEFINED_SYMBOLS[line] = address
                            address += 1
                        line = PREDEFINED_SYMBOLS[line]
                    line = int(line)  # Convert the string after @ to an integer
                    line = format(line, '016b')  # Convert to 16-bit binary format
                    lines.append(line)
                    counter += 1
                    print(line)
                else:
                    if line[1] == '=' or line[2] == '=':
                        parsed = line.split('=')  # Split the line into destination and address part
                        dest = DEST_MNEMONIC_TO_BITS[parsed[0]]
                        comp = COMP_MNEMONIC_TO_BITS[parsed[1]]
                        if ";" in line:
                            parsed = line.split(';')
                            jump = JUMP_MNEMONIC_TO_BITS[parsed[1]]
                        else:
                            jump = '000'
                        line = C_COMMAND_INIT_BITS + comp + dest + jump
                        lines.append(line)
                        counter += 1
                        print(line)
                    elif line[1] == ';':
                        parsed = line.split(';')
                        comp = COMP_MNEMONIC_TO_BITS[parsed[0]]
                        jump = JUMP_MNEMONIC_TO_BITS[parsed[1]]
                        dest = '000'
                        line = C_COMMAND_INIT_BITS + comp + dest + jump
                        lines.append(line)
                        counter += 1
                        print(line)

            # write filename.hack based on lines list
            with open(filename.replace('.asm', '.hack'), 'w') as file:
                for line in lines:
                    file.write(line + '\n')

# Ensures the main function is called only when this script is executed directly
if __name__ == "__main__":
    main()