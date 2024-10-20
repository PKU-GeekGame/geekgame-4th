def parse_fm2(line: str):
    if not line.startswith('|0'):
        return None

    input_byte = 0b00000000
    if 'A' in line:
        input_byte |= 0b00000001
    if 'B' in line:
        input_byte |= 0b00000010
    if 'S' in line:
        input_byte |= 0b00000100
    if 'T' in line:
        input_byte |= 0b00001000
    if 'U' in line:
        input_byte |= 0b00010000
    if 'D' in line:
        input_byte |= 0b00100000
    if 'L' in line:
        input_byte |= 0b01000000
    if 'R' in line:
        input_byte |= 0b10000000
    return input_byte


def convert(fm2_file, output_file):
    with open(fm2_file, 'r') as fm2, open(output_file, 'wb') as output:
        for line in fm2:
            input_byte = parse_fm2(line)
            if input_byte is not None:
                output.write(input_byte.to_bytes(1, byteorder='little'))


if __name__ == "__main__":
    fm2_file = "fm2.fm2"
    output_file = "bin.bin"
    convert(fm2_file, output_file)
