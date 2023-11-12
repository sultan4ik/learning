def make_readable(seconds):
    return f'{(seconds // 3600):02}:{(seconds % 3600 // 60):02}:{(seconds % 3600 % 60):02}'


def main():
    make_readable(0)
    make_readable(5)
    make_readable(60)
    make_readable(86399)
    make_readable(359999)


if __name__ == '__main':
    main()
