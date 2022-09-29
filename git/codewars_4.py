class RomanNumerals:
    translator = {1:'I', 2:'II', 3:'III', 4:'IV', 5:'V', 6:'VI', 7:'VII', 8:'VIII', 9:'IX', 10:'X',
                  50:'L', 100:'C', 500:'D', 1000:'M'}

    def to_roman(val):
        result = ''
        thousands = val // 1000
        result += thousands*'M'


    def from_roman(roman_num):
        return 0


RomanNumerals.to_roman(1000)
RomanNumerals.to_roman(4)
RomanNumerals.to_roman(1)
RomanNumerals.to_roman(1990)
RomanNumerals.to_roman(2008)