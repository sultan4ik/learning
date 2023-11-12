def domain_name(url):
    i = 0
    k = 0
    one_step = url.split('/')
    while one_step[i] in ['http:', 'https:', 'www', '']:
        i += 1
    two_step = one_step[i].split('.')
    while two_step[k] in ['http:', 'https:', 'www', '']:
        k += 1
    return two_step[k]


def main():
    pass


if __name__ == '__main':
    main()
