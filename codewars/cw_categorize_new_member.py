def open_or_senior(data):
    result = []
    for i in data:
        if i[0] > 54 and i[1] > 7:
            result.append('Senior')
        else:
            result.append('Open')
    return result


def main():
    pass


if __name__ == '__main':
    main()
