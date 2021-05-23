import json
import pandas as pd


with open('capitalStations.json', encoding='utf-8-sig')as json_file:  #Open Saved Json file to Dictionary
    stations = json.load(json_file)

#역의 Line 정보 저장
stations_info = {}
for _ in stations:
    stations_info[_['name']]=_['lines']

transfer=[]
transfer_time = {}

#환승정보 Dictionary 생성 및 기본값 2.0으로 초기화
for _ in stations:
    if len(_['lines'])!=1:

        transfer.append(_)
        tmp_dict ={}

        for i in _['lines']:
            tmp_sub_dict = {}
            for k in _['lines']:
                if(i!=k):
                    tmp_sub_dict[k]=float(2)
            tmp_dict[i]=tmp_sub_dict
        transfer_time[_['name']] = tmp_dict

#역의 환승정보가 저장된 csv 파일 Read
transfer_data = pd.read_csv('./환승.csv',encoding='utf-8') #Load the csv File


#csv를 토대도 환승정보 저장
for index in range(len(transfer_data['역명'])):
    try:
        name = transfer_data['역명'][index]
        where = transfer_data['호선'][index]
        trans = transfer_data['환승노선'][index]
        time = transfer_data['걸리는시간'][index]

        transfer_time[name][trans][where]=time
    except:
        pass

#역의 노선 정보 json dump
with open('./stations_info.json','w',encoding='UTF-8-sig') as f:
    json.dump(stations_info,f,ensure_ascii = False)
#환승정보 json dump
with open('./transfer_data.json','w',encoding='UTF-8-sig') as f:
    json.dump(transfer_time,f,ensure_ascii = False)



#역 정보 json load
with open('stations.json', encoding='utf-8-sig')as json_file:  #Open Saved Json file to Dictionary
    stations = json.load(json_file)


csv_data = pd.read_csv('./역간거리데이터 - 경의중앙선-2.csv',encoding='utf-8') #Load the csv File



for i in range (len(csv_data['역명'])):  #Add time to go around stations
    if i==0:
        stations[csv_data['역명'][i]][csv_data['역명'][i+1]] = float(csv_data['걸리는시간'][i])
    else:
        tmp_name = csv_data['역명'][i-1]
        tmp_time = csv_data['걸리는시간'][i]

        stations[tmp_name][csv_data['역명'][i]] = float(tmp_time)

for i in range(len(csv_data['역명'])-1,0,-1):
    if csv_data['역명'][i] == csv_data['역명'][len(csv_data)-1]:
        stations[csv_data['역명'][i]][csv_data['역명'][i-1]] = float(csv_data['걸리는시간'][i])
        continue
    else:
        tmp_name = csv_data['역명'][i]
        tmp_time = csv_data['걸리는시간'][i]
        stations[tmp_name][csv_data['역명'][i-1]] = float(tmp_time)


#Save the newest json File
with open('./stations.json','w',encoding='UTF-8-sig') as f:
    json.dump(stations,f,ensure_ascii = False)
