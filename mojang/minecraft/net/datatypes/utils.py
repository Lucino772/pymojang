def position_to_int(x: int, z: int, y: int):
    return ((x & 0x3FFFFFF) << 38) | ((z & 0x3FFFFFF) << 12) | (y & 0xFFF)


def int_to_position(value: int):
    x, z, y = value >> 38, (value >> 12) & 0x3FFFFFF, value & 0xFFF

    if x >= 1 << 25:
        x -= 1 << 26
    if y >= 1 << 11:
        y -= 1 << 12
    if z >= 1 << 25:
        z -= 1 << 26

    return x, z, y
