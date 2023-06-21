def solution(args):
    i = 0
    buffer = 0
    result = ''
    while i != len(args):
        if i != len(args) - 1 and args[i] == args[i + 1] - 1:
            buffer += 1
        else:
            if buffer > 1:
                result += f'{args[i - buffer]}-{args[i]},'
            elif buffer == 1:
                result += f'{args[i - buffer]},{args[i]},'
            else:
                result += f'{args[i]},'
            buffer = 0
        i += 1
    print(result[:-1])


solution([-6, -3, -2, -1, 0, 1, 3, 4, 5, 7, 8, 9, 10, 11, 14, 15, 17, 18, 19, 20])
solution([-3, -2, -1, 2, 10, 15, 16, 18, 19, 20])