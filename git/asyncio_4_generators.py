from time import time


def gen_filename():
    while True:
        pattern = 'file-{}.jpeg'
        t = int(time() + 1000)
        yield pattern.format(str(t))


def generation_one(s):
    for i in s:
        yield i


def generation_two(n):
    for i in range(n):
        yield i


g1 = generation_one('artur')
g2 = generation_two(5)

tasks = [g1, g2]

while tasks:
    task = tasks.pop(0)

    try:
        i = next(task)
        print(i)
        tasks.append(task)
    except StopIteration:
        pass