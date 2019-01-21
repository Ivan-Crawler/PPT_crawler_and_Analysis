#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 12:22:00 2019

@author: cheating
"""

import pandas as pd
import numpy as np
import jieba
jieba.set_dictionary('dict.txt.big')


# 無意義字元列表，可以自行新增
removeword = ['span','class','f3','https','imgur','h1','_   blank','href','rel',
              'nofollow','target','cdn','cgi','b4','jpg','hl','b1','f5','f4',
              'goo.gl','f2','email','map','f1','f6','__cf___','data','bbs'
              'html','cf','f0','b2','b3','b5','b6','原文內容','原文連結','作者'
              '標題','時間','看板','<','>','，','。','？','—','閒聊','・','/',
              ' ','=','\"','\n','」','「','！','[',']','：','‧','╦','╔','╗','║'
              ,'╠','╬','╬',':','╰','╩','╯','╭','╮','│','╪','─','《','》','_'
              ,'.','、','（','）','　','*','※','~','○','”','“','～','@','＋']

#設定你關心的影劇名稱
movie = ['成為王的男人',
        '皇后的品格',
        '赤月青日',
        '神的測驗',
        '死之詠讚',
        '王牌大律師',
        'Priest驅魔者',
        '加油吧威基基',
        '皮諾丘',
        '魔女寶鑑',
        '好運羅曼史',
        '購物王路易',
        '七次初吻',
        '男朋友',
        '請回答1997',
        '來自星星的你']

KoreaDrama=pd.read_csv('KoreaDrama.csv') #開啟檔案


#紀錄30天，各各影集的數量
remeber_movie= []
for j in movie:
    themovie=[]
    for i in range(31):
        #篩選一天的資料
        thebroadDF = KoreaDrama[KoreaDrama['時間']>=20181200 + i]
        thebroadDF = thebroadDF[thebroadDF['時間']<20181200 + i + 1]
        #確保有資料內容
        if len(thebroadDF) >0:
            theSTR = thebroadDF['標題'].sum() + thebroadDF['內容'].sum()
    
            # 移除無意義字元列
            for word in removeword:
                theSTR = theSTR.replace(word,'')
            
            #進行切詞
            words = list(jieba.cut(theSTR, cut_all=False))
        
            themovie.append(words.count(j))
        else:
            themovie.append(0)
    remeber_movie.append(themovie)

#加總31天，16個影集「總共」提到的次數（未下面百分比準備）    
listgetm=[]
for change in range(31):#30天
    getm = 0
    for cha in range(16):#16個影集
        getm += remeber_movie[cha][change]
    listgetm.append(getm)    

#開始計算百分比
for a in range(16):#16個影集
    for b in range(31):#30天
        if listgetm[b] != 0:#避免有除以0的狀況
            remeber_movie[a][b] = remeber_movie[a][b] / listgetm[b] *100
    
#繪圖
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as mplcm
import matplotlib.colors as colors # 設定圖的顏色
# 2. 設定中文字體路徑，如果產出文字雲無法顯示中文代表字體沒有指定成功
# 路徑如果只有檔名稱就代表字體檔與python 檔必須放在同個資料夾中
font_path = matplotlib.font_manager.FontProperties(fname='微软正黑体.ttf')
y = np.vstack(remeber_movie)#準備好y

#準備好畫布
fig, ax = plt.subplots()

#顏色處理
#顏色色盤網站：https://matplotlib.org/examples/color/colormaps_reference.html
NUM_COLORS = len(movie) #每個影集準備一種顏色
cm = plt.get_cmap('tab20') #指定色盤
cNorm  = colors.Normalize(vmin=-6, vmax=NUM_COLORS-1) #指定顏色的區間（最小、最大）
scalarMap = mplcm.ScalarMappable(norm=cNorm, cmap=cm) #將上述的設定值放入
ax.set_color_cycle([scalarMap.to_rgba(i) for i in range(NUM_COLORS)])#上色

#將數值資料放入
#要從最後一個影集開始畫，否則會被「蓋住」
ax.stackplot(range(1,32),100, labels=['來自星星的你']) #從最後一個開始畫
#從後面開始往回畫
for i in range(len(movie)-1,1,-1):
    ax.stackplot(range(1,32),sum(y[:i]), labels=[movie[15-i]])

ax.legend(loc='upper left',prop=font_path,bbox_to_anchor=(1.05,1.0))#圖例設定
plt.title("區域圖",fontproperties=font_path,fontsize=30)#標題
plt.ylabel("影劇聲量百分比",fontproperties=font_path,fontsize=15)#y的標題
plt.xlabel("天（2018年12月）",fontproperties=font_path,fontsize=15) #x的標題
plt.show()



#----------------------------------點陣圖--------------------------------------
#所有文章和標題都串在一起
theSTR = KoreaDrama['標題'].sum() + KoreaDrama['內容'].sum()
# 移除無意義字元列
for word in removeword:
    theSTR = theSTR.replace(word,'')
#切詞
words = list(jieba.cut(theSTR, cut_all=False))

#以影劇為單位，去計算每個影劇，在所有資料中的聲量
remeber_movie2= []
for j in movie:
    remeber_movie2.append(words.count(j))

avg=np.mean(remeber_movie2)# 計算聲量的平均

# 豆瓣上面的評分
bean = [6.9, 7.5, 8.6, 7.8, 8.5, 9.3, 6.8, 8.6, 8.2, 5.9, 6.7, 7.2, 5.8, 7.0, 9.0, 8.3]
#繪圖
plt.figure()
#判斷四個象限所在的位置，來決定顏色
for i in range(len(bean)):
    if bean[i]>8 and remeber_movie2[i] >avg:#第一象限
        color = 'blue'
    elif bean[i]>8 and remeber_movie2[i] <= avg:#第四象限
        color = 'green'
    elif bean[i]<=8 and remeber_movie2[i] > avg:#第三象限
        color = 'red'
    else:#第二象限
        color = 'black'
    plt.scatter(bean[i],remeber_movie2[i], color=color)
plt.axhline(avg, color='c', linestyle='dashed', linewidth=1) # 繪製平均線 
plt.axvline(8, color='c', linestyle='dashed', linewidth=1) # 繪製平均線    
plt.title("分佈圖",fontproperties=font_path,fontsize=30)#標題
plt.ylabel("影劇聲量",fontproperties=font_path,fontsize=15)#y的標題
plt.xlabel("豆瓣評分",fontproperties=font_path,fontsize=15) #x的標題
plt.show()