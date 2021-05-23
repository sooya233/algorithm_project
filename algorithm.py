#!/usr/bin/env python
# coding: utf-8


'''
전역변수들
1. 역과 주변역 정보 및 시간을 저장할 stations 변수
stations = {'역명': {'주변역' : 시간, '주변역' : 시간}, '역명' : {'주변역' : 시간, '주변역' : 시간}, ......}
'''

stations = {'충무로':{'동대입구' : 2, '을지로3가' : 2, '동대문역사문화공원' : 2, '명동' : 2},
'잠실':{'잠실새내':1.2, '잠실나루':1,'몽촌토성':0.8, '석촌':1.2},
'마포구청':{'망원':1, '월드컵경기장':0.8},
'강동구청':{'천호':0.9,'몽촌토성':1.6},
'잠실나루':{'잠실':1,'강변':2.3},
'강변':{'잠실나루':2.3,'구의':1.6},
'잠실새내':{'잠실':1.2,'종합운동장':2.3},
'종합운동장':{'잠실새내':2.3,'삼성':2.1},
'삼성':{'종합운동장':2.1,'선릉':4.0}}

def backtracking(station, n, time, visited = []):
    if time > n: return #소요시간이 n분을 넘어갈 경우 해당 역은 탐색하지 않는다
    
    #stations에 해당 역명이 없을 경우 탐색을 종료한다
    try:
        around_stations = stations[station]
    except KeyError:
        return
    visited.append(station) #station을 방문
    
    for st_name, takes_time in around_stations.items():#주변 역들 탐색
        if st_name in visited:
            continue
        backtracking(st_name, n, time + takes_time, visited)
    return visited

def main():
    start = input("input your station : ")
    limit = 5
    station_list = backtracking(start, limit, 0.0, [])
    print(limit, "분 안에 갈 수 있는 역 : ", station_list)

if __name__ == '__main__':
    main()





