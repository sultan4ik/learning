import numpy as np


def snail(snail_map):
    np_array = np.array(snail_map)
    dimension = len(snail_map)
    result = np_array[0, :]
    while result != len(snail_map)**2:
        result.append(np_array[:, dimension - 1])
        result.append(np_array[dimension - 1:, dimension - 1])


array_1 = [[1,2,3],
         [4,5,6],
         [7,8,9]]
snail(snail_map = array_1)
array_2 = [[1,2,3],
         [8,9,4],
         [7,6,5]]
snail(snail_map = array_2)