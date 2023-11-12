
input()
points_list = [int(point) for point in input().split() if point != '0']
summary_list = [primary_point**2 + sum(points_list[index + 1:index + 1 + primary_point]) for index, primary_point in enumerate(points_list)]
print(summary_list)
print(sum(summary_list))
