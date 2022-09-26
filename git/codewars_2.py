import numpy as np


def snail(snail_map):
    np_array = np.array(snail_map)
    dimension = len(snail_map)
    result = np_array[0, :]
    k = 0
    # while len(result) != len(snail_map) ** 2:
    res_1 = np_array[k:k + 1, k:dimension]
    res_2 = np_array[k + 1:dimension, dimension - 1:dimension]
    res_3 = np_array[dimension - 1:dimension, k:dimension - 1]
    res_4 = np_array[k + 1:dimension - 1, k:k + 1]
    print(res_1, res_2, res_3, res_4)


array_2 = [[1,2,3],
         [8,9,4],
         [7,6,5]]
snail(snail_map = array_2)