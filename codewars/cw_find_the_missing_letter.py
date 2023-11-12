def find_missing_letter(chars):
    i = 0
    while ord(chars[i]) == ord(chars[i + 1]) - 1:
        i += 1
    return chr(ord(chars[i + 1]) - 1)


def main():
    pass


if __name__ == '__main':
    main()
