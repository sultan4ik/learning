def rgb(r, g, b):
    d = [r, g, b]
    for (i, _) in enumerate(d):
        if d[i] < 0:
            d[i] = 0
        elif d[i] > 255:
            d[i] = 255
    return f'{d[0]:02X}{d[1]:02X}{d[2]:02X}'


def main():
    pass


if __name__ == '__main':
    main()
