def to_camel_case(text):
    list = "".join(['_' if ch == '-' else ch for ch in text]).split('_')
    return "".join(word if list.index(word) == 0 else word.title() for word in list)


def main():
    pass


if __name__ == '__main':
    main()
