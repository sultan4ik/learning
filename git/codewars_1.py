def valid_braces(string):
    braces_dict = {"(":[], ")":[], "[":[], "]":[], "{":[], "}":[]}
    i = 0
    for brace in string:
        braces_dict[brace].append(string.index(brace))
        i += 0
    sum_1 = [x1 - x2 for (x1, x2) in zip(braces_dict[")"], braces_dict["("]) if len(braces_dict[")"]) == len(braces_dict["("])]
    sum_2 = [x1 - x2 for (x1, x2) in zip(braces_dict["]"], braces_dict["["]) if len(braces_dict["]"]) == len(braces_dict["["])]
    sum_3 = [x1 - x2 for (x1, x2) in zip(braces_dict["}"], braces_dict["{"]) if len(braces_dict["}"]) == len(braces_dict["{"])]
    print(sum_1, sum_2, sum_3)
    sum_1.extend(sum_2)
    sum_1.extend(sum_3)
    print(sum_1)
    if len(sum_1) != 0:
        for value in sum_1:
            if value % 2 == 0 or value < 0:
                return False
        return True
    else:
        print(False)



# valid_braces(string="()")
# valid_braces(string="(}")
# valid_braces(string="[]")
# valid_braces(string="{}")
# valid_braces(string="[(])")
# valid_braces(string="{}()[]")
# valid_braces(string="([{}])")
# valid_braces(string="([}{])")
# valid_braces(string="{}({})[]")
valid_braces(string="(({{[[]]}}))")
# valid_braces(string="(((({{")
# valid_braces(string=")(}{][")
# valid_braces(string="())({}}{()][][")