# ROMANS = {
#     'M': 1000,
#     'CM': 900,
#     'D': 500,
#     'C': 100,
#     'XC': 90,
#     'L': 50,
#     'X': 10,
#     'V': 5,
#     'IV': 4,
#     'I': 1,
# }


class RomanNumerals:

    # def to_roman(n):
    #     s = ''
    #     for key, value in ROMANS.items():
    #         while n % value != n:
    #             n = n - value
    #             s += key
    #     print(s)

    def to_roman(val):
        result = ''
        translator = {1000: ['M'], 100: ['C', 'D', 'CD', 'CM'], 10: ['X', 'L', 'XL', 'XC'], 1: ['I', 'V', 'IV', 'IX']}
        for key in translator:
            if 4 * key > val >= key:
                result += val // key * translator[key][0]
            if 5 * key > val >= 4 * key:
                result += translator[key][2]
            if 10 * key > val >= 9 * key:
                result += translator[key][3]
            if 9 * key > val >= 5 * key:
                result += translator[key][1] + (val - 5 * key) // key * translator[key][0]
            val %= key
        return result

    def from_roman(roman_num):
        result = 0
        translator = {'CM': 900, 'CD': 400, 'XC': 90, 'XL': 40, 'IX': 9, 'IV': 4,
                      'M': 1000, 'D': 500, 'C': 100, 'L': 50, 'X': 10, 'V': 5, 'I': 1}
        for key in translator:
            while key in roman_num:
                result += translator[key]
                roman_num = roman_num.replace(key, '', 1)
        return result


RomanNumerals.to_roman(1000)
RomanNumerals.to_roman(4)
RomanNumerals.to_roman(1)
RomanNumerals.to_roman(1990)
RomanNumerals.to_roman(2008)
RomanNumerals.from_roman('XXI')
RomanNumerals.from_roman('I')
RomanNumerals.from_roman('IV')
RomanNumerals.from_roman('MMVIII')
RomanNumerals.from_roman('MDCLXVI')