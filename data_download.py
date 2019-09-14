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
import matplotlib.ticker as ticker
import pandas as pd
from datetime import datetime
import numpy as np
from windrose import WindroseAxes
from matplotlib.font_manager import FontProperties
from matplotlib.image import BboxImage
from matplotlib.transforms import Bbox,TransformedBbox
# =============================================================================
# print('相關站號及日期輸入請閱讀下載格式說明文件')
# #id = input("輸入id:")
id = '4008'
#date = input("請輸入日期:")
date = '20190903'
#pull the csv from database
# 
url='http://ec2-54-175-179-28.compute-1.amazonaws.com/get_csv_xitou.php?device_id='+str(id)+'&year_month='+str(date)
# print(url)
# 
r=requests.get(url)
# 
csv_LINK_PATTERN = 'href="(.*)">Download'
req = urllib.request.Request(url)
html = urllib.request.urlopen(req)
doc = html.read().decode('utf8')
print(doc)
url_list = list(set(re.findall(csv_LINK_PATTERN, doc)))
# 
string1 = "'>Download ID" + str(id) + str(date) +" Data</a><br>"
# 
get_rul_patten = doc.strip(string1).strip("<a href='")
# 
# 
file_name = get_rul_patten.strip('temp_file/').strip('.csv')
# 
server_path="http://ec2-54-175-179-28.compute-1.amazonaws.com/"+ get_rul_patten
# 
# # =============================================================================
# # 創建資料夾及儲存檔案
# # =============================================================================
#如果是檔案則處理
if not os.path.exists('./'+file_name):
    os.makedirs('./'+file_name)   # path 是”要建立的子目錄”
# 
urllib.request.urlretrieve(server_path,'./'+file_name+'/'+file_name+'.csv')
# 
# =============================================================================
#資料整理

local_csv_pos = './'+file_name+'/'+file_name+'.csv'

colum_id = ['id','time','weather','air','acceleration']
del_id = [0,2,4,6,8]
csv_data = pd.read_csv(local_csv_pos,sep=", |,, | = |= ",header=None)
csv_data.drop(del_id,axis=1, inplace=True)
csv_data.columns=colum_id

#1.氣象資料(溫度、大氣壓力、濕度、風速、風向、雨量)
wea = csv_data[['time','weather']]
wea_rel = wea['weather'].str.split(',',expand=True)
wea_adj= wea_rel.fillna('0')

#wea_rel.drop(30,axis=1, inplace=True)

#2.空氣品質(Mq131、MQ135、MQ136、)
air_qu = csv_data[['time','air']]
air_rel = air_qu['air'].str.split(',',expand=True)
air_adj= air_rel.fillna('0')
#air_rel.drop(30,axis=1, inplace=True)

#3.地表加速度
acc = csv_data[['time','acceleration']]
acc_rel = acc['acceleration'].str.split(':',expand=True)
acc_rel.drop(30,axis=1, inplace=True)
acc_adj =acc_rel.fillna('0')

#======TEST========
# =============================================================================
# y=wea_adj[4].astype(float).values
# x=wea_adj[3].astype(float).values
# 
# fig = plt.figure()
# ax = WindroseAxes.from_ax()
# ax.bar(y, x, normed=True, opening=0.8, edgecolor='white')
# ax.set_legend()
# plt.savefig('plot'+str(4)+'.png')
# 
# =============================================================================



# =============================================================================
# plot the data
# =============================================================================
# =============================================================================
# #weather data plot
title1 = ['tempeture','Atmospheric pressure','Humidity','Wind speed','Wind direation','Rainfaill']
unit1 = ['degree Celsius','hpa','%','m/s','direation','mm']
for i in range(wea_rel.shape[1]):
    if i !=4:
        y=wea_adj[i]
        x1=pd.to_datetime(wea['time'],format= '%Y%m%d%H%M%S')
#        plt.scatter(x1,y,c='m',s='30',alpha= .5,maker= 'D')
        plt.plot(x1,y,color='#900302',marker='+',linestyle='-')
        plt.xlabel('time', fontdict = {'fontsize':14})
        plt.ylabel(unit1[i], fontdict = {'fontsize':14})
        plt.title(title1[i], fontdict = {'fontsize':14})
        plt.xticks(rotation = 30)
        plt.yticks([])
        plt.xticks([])
#     plt.yticks(float(min(y)),float(max(y)),20)
        plt.savefig('./'+file_name+'/'+title1[i]+'.png', dpi= 300)
#       #  new_tick = np.linspace(int(min(y)),int(max(y)),20)
#         y = y.array(y)  
#         plt.ylim((float(max(y)), float(min(y)))
# #        plt.yticks(y.arange(min(y),max(y), step=0.1))
#         plt.savefig('./'+file_name+'/'+title1[i]+'.png', dip= 300)
        plt.show()
#         
    if not i !=4 :
         y=wea_adj[i].astype(float).values
         x=wea_adj[i-1].astype(float).values
         ax = WindroseAxes.from_ax()
         ax.bar(y, x, normed=True, opening=0.8, edgecolor='white')
         ax.set_legend()
         plt.title(title1[i], fontdict = {'fontsize':14})
         plt.savefig('./'+file_name+'/'+title1[i]+'.png', dpi= 300)
         plt.show()
# =============================================================================
# #quailty of the air data
# =============================================================================
title2 = ['Ozone','Fumes','Hydrogen Sulfide','Ammonia','Carbon monoxide','Nitrogen dioxide','Propane','Butane','Methane','Hydrogen','Ethanol','PM1','PM2.5','PM10']
unit2 = ['Voltage','Voltage','Voltage','ppm','ppm','ppm','ppm','ppm','ppm','ppm','ppm','μg/m3','μg/m3','μg/m3']
# 
for i in range(air_rel.shape[1]):
     y=air_adj[i]
     x2=pd.to_datetime(air_qu['time'],format= '%Y%m%d%H%M%S')
     aa=plt.plot(x2,y,'bo')
     plt.xlabel('time', fontdict = {'fontsize':14})
     plt.ylabel(unit2[i], fontdict = {'fontsize':14})
     plt.title(title2[i], fontdict = {'fontsize':14})
     plt.xticks(rotation = 30)
#     plt.gca().set(ylim=(float(min(y)),float(max(y))))
#     plt.set_yticks(y[::30])
     plt.yticks([])
     plt.xticks([])
#     plt.yticks(float(min(y)),float(max(y)),20)
     plt.savefig('./'+file_name+'/'+title2[i]+'.png', dpi= 300)
     plt.show()
# # =============================================================================
# =============================================================================
# #acceleration of the earthquake
# =============================================================================
# 
# =============================================================================
# y3=acc_rel.iloc[0]
# x3=pd.DataFrame(y3,columns=['count','value'])
# # =============================================================================
# plt.bar(x3,y3,align='center',width=0.5)
# plt.xlabel("(m^2/s^2)")
# plt.ylabel("(T)")
# plt.title("地表加速度")
# plt.savefig('./'+file_name+'/'+'plt.png')
# plt.show()
# =============================================================================
# =============================================================================
# 
# =============================================================================
# =============================================================================
















