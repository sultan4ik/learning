def accum(s):
    result = s[0].upper()
    i = 1
    while i < len(s):
        result = result + '-' + s[i].upper() + s[i].lower()*i
        i += 1
    return result


def main():
    pass


if __name__ == '__main':
    main()
