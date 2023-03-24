def isColorValidHEX(color):
    if len(color) != 7:
        return False
    if color[0] != '#':
        return False
    for i in range(1, 7):
        if color[i] not in '0123456789abcdef':
            return False
    return True

def isColorValidRGB(color):
    if len(color) != 3:
        return False
    for i in range(3):
        if color[i] < 0 or color[i] > 255:
            return False
    return True

def convertHexColorToRGB(color):
    return tuple(int(color[i:i+2], 16) for i in (1, 3, 5))

def convertRGBColorToHex(color):
    return '#%02x%02x%02x' % color