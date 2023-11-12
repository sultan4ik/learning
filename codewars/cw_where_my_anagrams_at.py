def anagrams(word, words):
    result = []
    for x in words:
        if sorted(word) == sorted(x):
            result.append(x)
    return result


def main():
    pass


if __name__ == '__main':
    main()
