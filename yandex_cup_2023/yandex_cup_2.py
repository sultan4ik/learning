import numpy as np

beacon_count = 3
beacon_a = [-5.0, -1.0, 9.0, 20.4694894905]
beacon_b = [4.0, -1.0, 9.0, 16.3095064303]
beacon_c = [-7.0, 6.0, 7.0, 19.9499373433]

first_line = [2*(beacon_b[0] - beacon_a[0]),
              2*(beacon_b[1] - beacon_a[1]),
              2*(beacon_b[2] - beacon_a[2])]
second_line = [2*(beacon_c[0] - beacon_b[0]),
              2*(beacon_c[1] - beacon_b[1]),
              2*(beacon_c[2] - beacon_b[2])]
third_line = [2*(beacon_a[0] - beacon_c[0]),
              2*(beacon_a[1] - beacon_c[1]),
              2*(beacon_a[2] - beacon_c[2])]

vector = [beacon_a[3]**2 - beacon_b[3]**2 + beacon_b[0]**2 - beacon_a[0]**2 + beacon_b[1]**2 - beacon_a[1]**2 + beacon_b[2]**2 - beacon_a[2]**2,
          beacon_b[3]**2 - beacon_c[3]**2 + beacon_c[0]**2 - beacon_b[0]**2 + beacon_c[1]**2 - beacon_b[1]**2 + beacon_c[2]**2 - beacon_b[2]**2,
          beacon_c[3]**2 - beacon_a[3]**2 + beacon_a[0]**2 - beacon_c[0]**2 + beacon_a[1]**2 - beacon_c[1]**2 + beacon_a[2]**2 - beacon_c[2]**2,]

array = np.array([first_line, second_line, third_line])
vector = np.array(vector)
print(array)
print(vector)

# try:
#     print(np.linalg.inv(array).dot(vector))
# except np.linalg.LinAlgError:
#     print('ХЕРНЯ!')
#     array = np.array([first_line, third_line])
#     vector = np.array(vector[:2])
#     print(array)
#     print(vector)
#     print(np.linalg.inv(array).dot(vector))
