# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 10:03:12 2019

@author: Luming
"""
import PyQt5
import requests
import urllib.request
import re
import os 
import matplotlib.pyplot as plt
import pandas as pd

print('相關站號及日期輸入請閱讀下載格式說明文件')
#id = input("輸入id:")
id = '4008'
#date = input("請輸入日期:")
date = '20190903'
#pull the csv from database

url='http://ec2-54-175-179-28.compute-1.amazonaws.com/get_csv_xitou.php?device_id='+str(id)+'&year_month='+str(date)
print(url)

r=requests.get(url)

csv_LINK_PATTERN = 'href="(.*)">Download'
req = urllib.request.Request(url)
html = urllib.request.urlopen(req)
doc = html.read().decode('utf8')
# print(doc)
url_list = list(set(re.findall(csv_LINK_PATTERN, doc)))

string1 = "'>Download ID" + str(id) + str(date) +" Data</a><br>"

get_rul_patten = doc.strip(string1).strip("<a href='")


file_name = get_rul_patten.strip('temp_file/').strip('.csv')

server_path="http://ec2-54-175-179-28.compute-1.amazonaws.com/"+ get_rul_patten

urllib.request.urlretrieve(server_path,file_name+'.csv')

#資料整理
local_csv_pos = file_name+'.csv'

colum_id = ['id','time','weather','air','acceleration']
del_id = [0,2,4,6,8]
csv_data = pd.read_csv(local_csv_pos,sep=", |,, | = |= ",header=None)
csv_data.drop(del_id,axis=1, inplace=True)
csv_data.columns=colum_id

#1.氣象資料
wea = csv_data[['time','weather']]
wea_rel = wea['weather'].str.split(',',expand=True)
#wea_rel.drop(30,axis=1, inplace=True)

#2.空氣品質
air_qu = csv_data[['time','air']]
air_rel = air_qu['air'].str.split(',',expand=True)
#air_rel.drop(30,axis=1, inplace=True)

#3.地表加速度
acc = csv_data[['time','acceleration']]
acc_rel = acc['acceleration'].str.split(':',expand=True)
acc_rel.drop(30,axis=1, inplace=True)

#畫圖
#