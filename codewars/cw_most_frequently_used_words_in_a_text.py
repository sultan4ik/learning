def top_3_words(text):
    result = []
    dict = {}
    list_from_text = "".join([ch if ch.isalpha() or ch == "'" else ' ' for ch in text]).lower().split()
    for value in list_from_text:
        if value in dict.keys():
            dict[value] += 1
        elif value.replace("'", "").isalpha():
            dict[value] = 1
    top_3_value = sorted(dict.values(), reverse=True)
    for top_3 in top_3_value:
        [result.append(keys) for keys, item in dict.items() if item == top_3 and keys not in result]
    return(result[0:3])


def main():
    pass


if __name__ == '__main':
    main()
