import json

with open('stations.json', encoding='utf-8-sig')as json_file:  #Open Saved Json file to Dictionary
    stations = json.load(json_file)
with open('stations_info.json', encoding='utf-8-sig')as json_file:  #Open Saved Json file to Dictionary
    stations_info = json.load(json_file)
with open('transfer_data.json', encoding='utf-8-sig')as json_file:  #Open Saved Json file to Dictionary
    transfer_data = json.load(json_file)

def getLine(st1, st2):
    line1 = stations_info[st1]
    line2 = stations_info[st2]
    
    link = []
    for num1 in line1:
        for num2 in line2:
            if num1 == num2:
                link.append(num1)
    return link

def backtracking(line, station, n, time, visited = {}): #start station은 line input을 ""로(empty string)
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
        next_time = time + takes_time #다음 역까지 걸린 시간
        link = getLine(station, st_name)
        for riding in link:
            if line == "": #출발역 예외처리
                backtracking(riding, st_name, n, next_time, visited)
            if riding == line:
                backtracking(riding, st_name, n, next_time + 0.5, visited) #정차시간 추가
            else:
                try:
                    transfer_time = transfer_data[station][line][riding]
                except KeyError:
                    continue
                backtracking(riding, st_name, n, next_time + 3.0 + transfer_time, visited) #정차시간 + 환승시간 + 대기시간
    st_list = list(visited.keys())
    return st_list

def getInput():
    n = int(input('How many people? '))
    station_list = []

    for i in range(n):
        temp = input('Input departure station: ')
        station_list.append(temp)
        
    return station_list, n

def bruteforce(accessible_list, n, cnt):
    duplicate_list = []
    for station in accessible_list[0]:
        duplicated = True
        for i in range(1, n): #accessible_list[i] 에 대하여 전수조사
            flag = False
            for st in accessible_list[i]:
                cnt = cnt + 1
                if st == station:
                    flag = True
                    break
            if flag == False:
                duplicated = False
                break
        if duplicated == False:
            continue
        duplicate_list.append(station)
    return duplicate_list, cnt            

def insertion_sort(arr, cnt):
    for end in range(1, len(arr)):
        for i in range(end, 0, -1):
            if arr[i - 1] > arr[i]:
                cnt = cnt + 1
                arr[i - 1], arr[i] = arr[i], arr[i - 1]
    return cnt

def binarySearch(accessible_list, station, cnt):
    size = len(accessible_list)
    left = 0
    right = size - 1
    
    while left <= right:
        mid = int((left + right) / 2)
        cnt = cnt + 1
        if accessible_list[mid] == station:
            return True
        elif accessible_list[mid] > station:
            right = mid - 1
        else:
            left = mid + 1
    return False

def binary(accessible_list, n, cnt):
    #1. accessible_list를 삽입정렬의 방식으로 sort한다
    for acc in accessible_list:
        cnt = cnt + insertion_sort(acc, 0)
        
    #2. accessible_list[0]에 나오는 역들을 기준으로 이진 탐색을 진행한다
    duplicate_list = []
    for station in accessible_list[0]:
        duplicated = True
        for i in range(1, n):
            duplicated = duplicated and binarySearch(accessible_list[i], station, cnt)
        if duplicated:
            duplicate_list.append(station)
    return duplicate_list, cnt

def hashing(accesible_list, n, cnt):
    #1. dictionary형태로 hashing 테이블을 구성한다
    table = []
    
    for i in range(len(accesible_list)):
        dic = {station : 1 for station in accesible_list[i]}
        cnt = cnt + len(accesible_list[i])
        table.append(dic)

    #2. 역들을 탐색한다
    duplicate_list = []
    for station in accesible_list[0]:
        duplicated = True
        for i in range(1, n):
            cnt = cnt + 1
            val = table[i].get(station)
            if val == None:
                duplicated = False
                break
        if duplicated:
            duplicate_list.append(station)
    return duplicate_list, cnt

def getList(accessible_list, n, method): #갈수있는 역들 모음(2차원배열), 사람 수
    duplicate_list, cnt = method(accessible_list, n, cnt=0)
    return duplicate_list, cnt

def solve(station_list, n, func):
    time = 5
    while True:
        accessible_list = []    
        
        #백트래킹으로 일정 시간 안에 갈 수 있는 역들을 찾는 부분
        for i in range(n):
            possible_station = backtracking("", station_list[i], time, 0.0, {})
            accessible_list.append(possible_station)
            
        dest_stations = []
        dest_stations, cnt = getList(accessible_list, n, method=func)
        if dest_stations: break
        else: time = time + 5
    
    #더 짧은 시간 안에 갈 수 있는 역들 재탐색
    for i in range(time - 1, time - 5, -1):
        accessible_list = []
        for j in range(n):
            possible_station = backtracking("", station_list[j], i, 0.0, {})
            accessible_list.append(possible_station)
        r_dest_stations, r_cnt = getList(accessible_list, n, method=func)
        if r_dest_stations:
            dest_stations = r_dest_stations
            cnt = r_cnt
            time = i
            continue
        else: break
    
    print("Recommand Station: ", dest_stations)
    print("Time Complexity: ", cnt)

def main():
    func_list = [bruteforce, binary, hashing]
    func_name = ['Brute-Force', 'Binary-Search', 'Hashing']
    station_list, n = getInput()
    print('==========================')
    
    for i in range(3):
        print(func_name[i])
        solve(station_list, n, func_list[i])
        print('==========================')

if __name__ == '__main__':
    main()


