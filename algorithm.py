#!/usr/bin/env python
# coding: utf-8


import json

with open('stations.json', encoding='utf-8-sig')as json_file:  #Open Saved Json file to Dictionary
    stations = json.load(json_file)

from collections import deque

def backtracking(station, n, time, visited = {}):
    #print(station, time)
    if time > n: return #소요시간이 n분을 넘어갈 경우 해당 역은 탐색하지 않는다
    
    around_stations = stations[station]
    if station in visited:
        if visited[station] > time:
            visited[station] = time
        else:
            return
    else:
        visited[station] = time
    
    for st_name, takes_time in around_stations.items():#주변 역들 탐색
        backtracking(st_name, n, time + takes_time + 0.5, visited) #0.5초 정차시간 추가?
    st_list = list(visited.keys())
    return st_list

def bfs(station, n, time, visited = []):
    queue = deque([(station, time)])
    while queue:
        st_info = queue.popleft()
        st_name = st_info[0]
        elapsed_time = st_info[1]
        
        try:
            around_stations = stations[st_name]
        except KeyError:
            continue
        visited.append(st_name)
        
        for next_name, takes_time in around_stations.items():
            if next_name in visited:
                continue
            next_time = elapsed_time + takes_time + 0.5 #0.5=정차시간
            if next_time <= n:
                queue.append((next_name, next_time))
    visited = set(visited)
    return visited

def getInput():
    n = int(input('사람이 몇 명입니까? '))
    station_list = []
    #n = 4
    #station_list = ['충무로', '선정릉', '잠실', '건대입구']
    #n = 1
    #station_list = ['잠실']
    
    for i in range(n):
        temp = input('탑승 역을 입력하시오: ')
        station_list.append(temp)
        
    return station_list, n

def binarySearch(accessible_list, station):
    size = len(accessible_list)
    left = 0
    right = size - 1
    
    while left <= right:
        mid = int((left + right) / 2)
        if accessible_list[mid] == station:
            return True
        elif accessible_list[mid] > station:
            right = mid - 1
        else:
            left = mid + 1
    return False

def getList(accessible_list, n): #갈수있는 역들 모음(2차원행렬), 사람 수
    duplicate_list = []
    for station in accessible_list[0]:
        duplicated = True
        for i in range(1, n):
            duplicated = duplicated and binarySearch(accessible_list[i], station)
        if duplicated:
            duplicate_list.append(station)
    return duplicate_list

def main():
    station_list, n = getInput()
    #accessible_list = []
    
    while True:
        accessible_list = []
        time = int(input("input time: "))
        if time == -1: break
    
        for i in range(n):
            possible_station = backtracking(station_list[i], time, 0.0, {})
            #print("=================================")
            possible_station = sorted(possible_station)
            accessible_list.append(possible_station)
    
        #print(accessible_list)
        dest_stations = []
        dest_stations = getList(accessible_list, n)

        print(dest_stations)
        #print(accessible_list)
        #for i in range(len(accessible_list[0]) - 1):
        #    print(accessible_list[0][i] < accessible_list[0][i+1])

if __name__ == '__main__':
    main()



