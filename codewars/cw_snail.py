import numpy as np


def snail(snail_map):
    np_array = np.array(snail_map)
    dimension = np_array.shape[1]
    result = []
    k = 0
    while dimension != 0:
        result.extend(np_array[k:k + 1, k:dimension].tolist()[0])
        result.extend(np_array[k + 1:dimension, dimension - 1:dimension].flatten().tolist())
        special_row = np_array[dimension - 1:dimension, k:dimension - 1].tolist()[0]
        special_column = np_array[k + 1:dimension - 1, k:k + 1].flatten().tolist()
        special_row.reverse()
        special_column.reverse()
        result.extend(special_row)
        result.extend(special_column)
        k += 1
        dimension -= 1
    print(result)


def main():
    array = [[1, 2, 3, 4],
             [12, 13, 14, 5],
             [11, 16, 15, 6],
             [10, 9, 8, 7]]
    snail(snail_map=array)


if __name__=='main':
    main()
