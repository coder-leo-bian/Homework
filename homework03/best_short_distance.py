import random
import matplotlib.pyplot as plt
import math


# x_ = [-77.28976849035128, -70.05883942758213, 54.85911680134504, 47.69907996174817, -44.57472172885175, 41.608305308328454, 59.1478618237505, 86.96834405309019, -8.558887604633597, 94.05533753742202, 11.848434908394026, -86.71821139233683, -28.863966511188963, 84.65786765306555, 44.645926054530435, -70.84638747753304, -35.0495271105691, -81.6490894506282, -11.25662192348642, -78.65528477020696]
# y_ = [-50.05197383050153, -60.12001601830861, 66.80968681040869, 4.35808623342875, 71.91875072854697, -40.656973574879544, -73.86024942374023, 5.599852641458298, 36.455255295375, -79.03458687377174, -72.76006663822032, 0.39483527732497237, -81.17351304798544, 61.2684867059796, -98.53211397112209, -19.853152865919085, -55.965864594719704, 27.644808577552112, -47.58562854937174, -43.680452908047315]
# index = [i for i in range(20)]

#
x = [-70.05883942758213, 54.85911680134504, 47.69907996174817, -44.57472172885175, 41.608305308328454]
y = [-50.05197383050153, -60.12001601830861, 66.80968681040869, 4.35808623342875, 71.91875072854697]
index = [i for i in range(5)]


record_distance = {}


def distance_between_two_points(path, point1, point2, c_and_i):
    if len(path) == 1:
        val = math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
        record_distance['->'.join([str(i) for i in c_and_i])] = val
        return val
    else:
        val = math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
        path = path + [c_and_i[-1]]
        key = '->'.join([str(i) for i in path])
        up_key = '->'.join([str(i) for i in path[: -1]])
        record_distance[key] = val + record_distance[up_key]
        return val + record_distance[up_key]


def best_short_distance(start, index):
    pathes = [[start]]
    closed = []
    all_path = []
    while pathes:
        path = pathes.pop(0)
        current_path = path[-1]
        for i in index:
            if current_path == i: continue
            elif current_path in path[: -1]: continue
            elif i in path: continue
            else: pass
            new_path = path + [i]
            pathes.append(new_path)
            if len(new_path) == len(index):
                all_path.append(new_path)
    return all_path


all_path_value = best_short_distance(0, index)


def best_sort_distance2(start, index):
    pathes = [[start]]
    while pathes:
        compare_distance = 0
        path = pathes.pop(0)
        current_path = path[-1]
        for i in index:
            if current_path == i:
                continue
            elif current_path in path[: -1]:
                continue
            elif i in path:
                continue
            else:
                pass
            distance = distance_between_two_points(path, (x[current_path], y[current_path]), (x[i], y[i]), [current_path, i])
            if not compare_distance or compare_distance > distance:
                compare_distance = distance
                new_path = path + [i]
            else:
                new_path = path + [i]
            pathes.append(new_path)
        # if len(new_path) == len(index):
        #     return new_path
    return '无'


best_path = best_sort_distance2(0, index)


def distance_between_two_points2(pathes):
    d = 0
    for i, v in enumerate(pathes[:-1]):
        d += math.sqrt((x[pathes[i]] - y[pathes[i]]) ** 2 + (x[pathes[i+1]] - y[pathes[i+1]]) ** 2)
    return d


bs = 0
bs_p = None
for path in all_path_value:
    d = distance_between_two_points2(path)
    print('{} ---> {}'.format(path, d))

    if not bs or bs > d:
        bs = d
        bs_p = path

print('*'*200)

print('{} ---> {}'.format(bs_p, bs))

print('*'*200)

print(best_path, distance_between_two_points2(best_path))
print(record_distance)
plt.Figure()
plt.scatter(x, y)
plt.show()

