import re
import json, requests
from collections import defaultdict
from operator import itemgetter


def deal_subway_data():
    with open('beijing.xml') as f:
        datas = f.read()
    pattern = re.compile('\s+lb="(\w+)"')
    station = re.findall(pattern, datas)
    pattern1 = re.compile('<l lid="\w+"\s+lb="(\w+)"')
    lines = re.findall(pattern1, datas)
    return station, lines


def subways_related(lines, station):
    subways = {}
    for i in range(len(lines)):
        if lines[i] == '机场线':
            pass
            # subways[lines[i]] = station[station.index(lines[i])+1:]
        else:
            subways[lines[i]] = station[station.index(lines[i])+1:station.index(lines[i+1])]
    subways['机场线'] = ['东直门', '三元桥', '3号航站楼', '2号航站楼']
    return subways


def graph_subway_lines(subways):
    # 地铁线关系图
    subway_line = defaultdict(list)
    for s1 in subways:
        for s2 in subways:
            if s1 == s2: continue
            if len(subways[s1][1:] + subways[s2][1:]) != len(set(subways[s1][1:] + subways[s2][1:])):
                subway_line[s1] = subway_line[s1] + [s2]
    return subway_line


def graph_subway_station(subways):
    # 地铁站关系图
    subway_station = {}
    for sub, vals in subways.items():
        for i, v in enumerate(vals):
            if v not in subway_station:
                if i == 0:
                    subway_station[v] = [vals[i + 1]]
                elif i == (len(vals) - 1):
                    subway_station[v] = [vals[i - 1]]
                else:
                    subway_station[v] = [vals[i - 1], vals[i + 1]]
            else:
                if i == 0:
                    subway_station[v] = subway_station[v] + [vals[i + 1]]
                elif i == (len(vals) - 1):
                    subway_station[v] = subway_station[v] + [vals[i - 1]]
                else:
                    subway_station[v] = subway_station[v] + [vals[i - 1], vals[i + 1]]

    return subway_station


def check_better_lines(start_to_stop, all_lines):
    """筛选最优路线"""
    better_lines = []
    all_lines = sorted(all_lines, key=lambda s: start_to_stop[0])
    for ss in start_to_stop:
        best_line = None
        for line in all_lines:
            if line[0] == ss[0] and line[-1] == ss[-1]:
                if not best_line:
                    best_line = line
                elif len(line) < len(best_line):
                    best_line = line
                elif len(line) == len(best_line):
                    better_lines.append(best_line)
                    best_line = line
        if best_line:
            better_lines.append(best_line)
    return better_lines


def search_lines_graph(start_station_line, stop_station_line, subway_line):
    """搜索并筛选最优换成线图(以每条地铁线为维度)"""
    start_to_stop, all_lines = [], []
    for start_line in start_station_line:
        for stop_line in stop_station_line:
            start_to_stop.append([start_line, stop_line])
            if start_line == stop_line:
                return [[start_line, stop_line]]

    print('开始和结束地铁线：{}'.format(start_to_stop))
    for line in start_to_stop:
        pathes = [[line[0]]]
        seened = []
        while pathes:
            path = pathes.pop(0)
            station = path[-1]
            if station in seened and station == line[1]: continue
            for successor in subway_line[station]:
                if successor in seened: continue
                if successor not in start_station_line:
                    new_path = path + [successor]
                    pathes.append(new_path)
                    if successor == line[1]:
                        if new_path not in all_lines:
                            all_lines.append(new_path)
            seened.append(station)
    better_lines = check_better_lines(start_to_stop, all_lines)
    return better_lines


def search_station_graph(start, stop, better_lines, subways):
    """按照每一站进一步筛选最优路线"""
    best_lines = []
    for line in better_lines:
        subway = {key: subways[key] for key in line}
        station_graph = graph_subway_station(subway)
        pathes = [[start]]
        seened = []
        while pathes:
            path = pathes.pop(0)
            station = path[-1]
            if station == '知春路':
                print(station)
            if station in seened and station == stop: continue
            for successor in station_graph[station]:
                if station == stop:
                    break
                if successor in seened: continue
                new_path = path + [successor]
                pathes.append(new_path)
                if successor == stop:
                    best_lines.append({'/'.join(line): new_path})
            if station != stop:
                seened.append(station)
    return best_lines


def search(start, stop, subways, subway_line, subway_station, sortfunction=None):
    """搜索返回最优路线"""
    start_station_line = []
    stop_station_line = []
    for subway_key, subway_values in subways.items():
        if start in subway_values:
            start_station_line.append(subway_key)
        if stop in subway_values:
            stop_station_line.append(subway_key)

    better_lines = search_lines_graph(start_station_line, stop_station_line, subway_line)

    best_lines = search_station_graph(start, stop, better_lines, subways)

    return sortfunction(best_lines)  if sortfunction else best_lines



def shortest_transfer_sort(best_lines):
    mid_dict = {key: value for x in best_lines for key, value in x.items()}
    mid_list = sorted(mid_dict.items(), key=lambda x: len(x[1]))
    best_lines = [{x[0]: x[1]} for x in mid_list]
    return best_lines


def main(start, stop, sortfunction=None):
    station, lines = deal_subway_data()
    subways = subways_related(lines, station) # 每条线对应的地铁站
    subway_line = graph_subway_lines(subways) # 每条地铁线的关系图
    subway_station = graph_subway_station(subways) # 每一站的换乘关系图
    best_lines = search(start, stop, subways, subway_line, subway_station, sortfunction)
    return best_lines


if __name__ == '__main__':
    for i in main('天安门西', '青年路', shortest_transfer_sort):
        print(i)



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

prin