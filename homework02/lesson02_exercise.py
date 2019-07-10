import re
import json, requests


def deal_subway_data():
    with open('../beijing.xml') as f:
        datas = f.read()
    pattern = re.compile('\s+lb="(\w+)"')
    station = re.findall(pattern, datas)
    pattern1 = re.compile('<l lid="\w+" lb="(\w+)"')
    lines = re.findall(pattern1, datas)
    lines.insert(6, '8号线北')
    lines.insert(7, '8号线南')
    return station, lines

station, lines = deal_subway_data()



# def subway_location_func(address):
#     # 获取地铁站坐标值
#     params = {'address': address,
#                       'city': '北京',
#                       'key': 'c498f052ee8837679469e79f9f9dd400'}
#     request = requests.request('get', url='https://restapi.amap.com/v3/geocode/geo?', params=params)
#     r = json.loads(request.text)
#     try:
#         return r['geocodes'][0]['location']
#     except Exception as e:
#         print(address)
#         return None
#
# subway_location = {}
# for s in station:
#     if s not in lines and s not in subway_location:
#         x_y = subway_location_func(s)
#         if x_y:
#             location = tuple(x_y.split(','))
#         else:
#             x_y = subway_location_func(s+'地铁站')
#             if not x_y:
#                 continue
#             location = tuple(x_y.split(','))
#         subway_location[s] = location if location else (0, 0)
#
# subway_location['德茂'] = ('116.435524', '39.980470')
# subway_location['紫草坞'] = ('116.403070', '39.933814')
# subway_location['万安'] = ('116.160356', '40.067916')
# subway_location['茶棚'] = ('116.403070', '39.933814')
#

#
# for k, v in subway_location.items():
#     subway_location[k] = (float(v[0]), float(v[1]))


def subways_related(lines, station):
    subways = {}
    for i in range(len(lines)):
        if lines[i] == '机场线':
            subways[lines[i]] = station[station.index(lines[i])+1:]
        else:
            subways[lines[i]] = station[station.index(lines[i])+1:station.index(lines[i+1])]

    subway_map = {}
    for sub, vals in subways.items():
        for i, v in enumerate(vals):
            if v not in subway_map:
                if i == 0:
                    subway_map[v] = [vals[i + 1]]
                elif i == (len(vals) - 1):
                    subway_map[v] = [vals[i - 1]]
                else:
                    subway_map[v] = [vals[i - 1], vals[i + 1]]
            else:
                if i == 0:
                    subway_map[v] = subway_map[v] + [vals[i + 1]]
                elif i == (len(vals) - 1):
                    subway_map[v] = subway_map[v] + [vals[i - 1]]
                else:
                    subway_map[v] = subway_map[v] + [vals[i - 1], vals[i + 1]]

    return subway_map

subway_map = subways_related(lines, station)


def search(start, stop, subway_map):
    pathes = [[start]]
    visited = []
    all_pathes = []
    while pathes:
        print(len(pathes))
        path = pathes.pop(0)
        current_station = path[-1]
        # if current_station in visited: continue
        for succ in subway_map[current_station]:
            if succ in path and succ in visited: continue
            new_path = path + [succ]
            # if new_path not in pathes:
            pathes.append(new_path)
            if succ == stop:
                all_pathes.append(new_path)
        visited.append(current_station)
    return all_pathes


for i in (search('十里河', '西二旗', subway_map)):
    print(i)