def add_num(seq, num):
    for i in range(len(seq)):
        seq[i] += num


origin = [3, 6, 2, 6]
add_num(origin, 3)

print(origin)