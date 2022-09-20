def valid_braces(string):
    while '[]' in string or '()' in string or '{}' in string:
        string = string.replace('()', '').replace('{}', '').replace('[]', '')
    return string == ''

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