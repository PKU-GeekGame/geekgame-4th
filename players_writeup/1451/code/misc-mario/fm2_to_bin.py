BUTTONS = ['A', 'B', 'S', 'T', 'U', 'D', 'L', 'R']


def int_to_input(i: int) -> str:
    '''
    Converts a byte to a string of 8 buttons.
    '''
    buttons = ''.join(BUTTONS[b] if (i & (1 << b)) else '.'
                      for b in range(7, -1, -1))
    return f'|0|{buttons}|........||\n'


def fm2_to_bin(fm2_file: str, offset: int):
    reverse_buttons = {}
    for idx, char in enumerate(BUTTONS):
        reverse_buttons[char] = idx

    bytes = b''
    with open(fm2_file, "r", encoding="utf-8") as f:
        for _ in range(offset):
            f.readline()
        for line in f.readlines():
            button_string = line[3:11]
            result = 0

            for index, char in enumerate(button_string):
                if char != '.':
                    result |= (1 << (7 - index))
            assert int_to_input(result)[3:11] == button_string
            bytes += result.to_bytes(1)
        # 给 flag1 补点帧，肉眼盯了个 18400 帧作为结束
        for _ in range(18400-17953):
            bytes += (0).to_bytes(1)
    return bytes


if __name__ == '__main__':
    with open("flag1.bin", 'wb') as f:
        f.write(fm2_to_bin("./7463.fm2", 15))
    with open("flag2.bin", 'wb') as f:
        f.write(fm2_to_bin("./5523.fm2", 15))
