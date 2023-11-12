def parse_int(string):
    zero_to_hundred = {'zero':0, 'one':1, 'two':2, 'three':3, 'four':4, 'five':5, 'six':6, 'seven':7, 'eight':8,
                       'nine':9, 'ten':10, 'eleven':11, 'twelve':12, 'thirteen':13, 'fourteen':14, 'fifteen':15,
                       'sixteen':16, 'seventeen':17, 'eighteen':18, 'nineteen':19, 'twenty':20, 'thirty':30, 'forty':40,
                       'fifty':50, 'sixty':60, 'seventy':70, 'eighty':80, 'ninety':90}
    hundred_to_million = {'hundred':100, 'thousand':1000, 'million':1000000}
    result = []
    summa = 0
    new_str = string.split()
    if 'thousand' in new_str:
        new_str.insert(new_str.index('thousand') + 1, 'del')
    new_str = " ".join([value for value in new_str])
    for value in new_str.split('del'):
        list = "".join([' ' if ch == '-' else ch for ch in value])
        for digit in list.split():
            if digit in zero_to_hundred.keys():
                summa += zero_to_hundred[digit]
            if digit in hundred_to_million.keys():
                summa *= hundred_to_million[digit]
        result.append(summa)
        summa = 0
    return sum(result)


def main():
    pass


if __name__ == '__main':
    main()
