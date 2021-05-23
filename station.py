import json
import pandas as pd

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
