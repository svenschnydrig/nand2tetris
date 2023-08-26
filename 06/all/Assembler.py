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

def get_cleaned_lines(filename):
    """Returns a list of cleaned lines from the given .asm file."""
    cleaned_lines = []
    
    with open(filename, 'r') as file:
        for line in file:
            # Removing whitespace and comments
            line = line.strip().replace(" ", "").split("//")[0]
            if line:
                cleaned_lines.append(line)
    return cleaned_lines

def first_pass(lines, symbols):
    """Processes the given lines for the first pass."""
    counter = 0
    for line in lines:
        if line[0] == '@':
            counter += 1
        elif line[0] == '(':
            label = line.replace('(', '').replace(')', '')
            symbols[label] = counter
        else:
            counter += 1

def second_pass(lines, symbols):
    """Processes the given lines for the second pass."""
    address = 16
    for line in lines:
        if line[0] == '@' and not line[1].isdigit():
            symbol = line[1:]
            if symbol not in symbols:
                symbols[symbol] = address
                address += 1

def process_a_command(line, symbols):
    """Processes and returns the binary string for an A-command."""
    value = line[1:]
    if not value.isdigit():
        value = symbols[value]
    return format(int(value), '016b')

def process_c_command(line, dest_mnemonic, comp_mnemonic, jump_mnemonic):
    """Processes and returns the binary string for a C-command."""
    if "=" in line:
        dest, remainder = line.split('=')
        comp, jump = remainder.split(';') if ';' in remainder else (remainder, '000')
    else:
        dest, jump = '000', line.split(';')[1]
        comp = line.split(';')[0]

    return '111' + comp_mnemonic[comp] + dest_mnemonic[dest] + jump_mnemonic[jump]

def main():
    # Ensures proper command line arguments are provided
    if len(sys.argv) < 2:
        print("Please provide the .asm filename as a command-line argument.")
        sys.exit(1)

    filename = sys.argv[1]
    symbols = dict(PREDEFINED_SYMBOLS)  # Assuming PREDEFINED_SYMBOLS is a dictionary

    # Reading and cleaning up the file content
    lines = get_cleaned_lines(filename)

    # First and Second pass
    first_pass(lines, symbols)
    second_pass(lines, symbols)

    # Processing commands and writing to output file
    output_lines = []
    for line in lines:
        if line[0] == '@':
            output_lines.append(process_a_command(line, symbols))
        elif line[0] != '(':
            output_lines.append(process_c_command(line, DEST_MNEMONIC_TO_BITS, COMP_MNEMONIC_TO_BITS, JUMP_MNEMONIC_TO_BITS))

    with open(filename.replace('.asm', '.hack'), 'w') as file:
        for line in output_lines:
            file.write(line + '\n')

if __name__ == "__main__":
    main()