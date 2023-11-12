def valid_braces(string):
    while '[]' in string or '()' in string or '{}' in string:
        string = string.replace('()', '')
        string = string.replace('{}', '')
        string = string.replace('[]', '')
    if string:
        return False
    else:
        return True


def main():
    valid_braces(string="()")
    valid_braces(string="(}")
    valid_braces(string="[]")
    valid_braces(string="{}")
    valid_braces(string="[(])")
    valid_braces(string="{}()[]")
    valid_braces(string="([{}])")
    valid_braces(string="([}{])")
    valid_braces(string="{}({})[]")
    valid_braces(string="(({{[[]]}}))")
    valid_braces(string="(((({{")
    valid_braces(string=")(}{][")
    valid_braces(string="())({}}{()][][")


if __name__ == '__main':
    main()
