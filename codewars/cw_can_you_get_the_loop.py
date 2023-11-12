def loop_size(node):
    list = []
    while node.__hash__() not in list:
        list.append(node.__hash__())
        node = node.next
    return len(list) - list.index(node.__hash__())


def main():
    pass


if __name__ == '__main':
    main()
