from turtle import clear
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import random as r
import csv
import numpy as np

# ni nak extract country indonesia
# df = pd.read_csv("starbucks_2018_11_06.csv")
# # print(df.head(3))

#to check state from Indonesia
# indonesia = df.loc[df['state']=="ID"]
# indonesia = indonesia.reset_index()
# # print(indonesia)
# indonesia.to_csv('indonesia_starbucks_2018_11_06.csv')

# print(d_indonesia)
# randomGeneratedStore =[r.random(d_indonesia) for x in range(10)]
# rrrr = r.random(d_indonesia[0])
# print(rrrr)
# for x in range(10):
#     randomGeneratedStore.append(r.random())


#create base map
# m = folium.Map(location=[0.7893,113.9213],tiles="OpenStreetMap",zoom_start= 5)

# markerCluster = MarkerCluster().add_to(m)
# # #nak plot location indonesia
# df = pd.read_csv('indonesia_starbucks_2018_11_06.csv')
# for i,row in df.iterrows():
#     lat = df.at[i,'latitude']
#     lng = df.at[i,'longitude']
#     store = df.at[i,'name']

#     popup = df.at[i,'name'] + '<br>' + str(df.at[i,'street_address']) + '<br>' + str(df.at[i,'zip_code']) + '<br>' + str(df.at[i,'city']) 

#     folium.Marker(location=[lat,lng],popup=popup,icon=folium.Icon(color='blue')).add_to(markerCluster)

# m.save('INDONESIA.html')

#first random

with open("indonesia_starbucks_2018_11_06.csv") as csvfile:
    reader = csv.reader(csvfile)
    data_indonesia=np.array([row for row in reader])

# print(data_indonesia)

randomGeneratedIndonesia = data_indonesia[np.random.choice(data_indonesia.shape[0],size=5,replace=False),:]
# randomGeneratedIndonesia = data_indonesia[randow_indices,:]
print(randomGeneratedIndonesia)

#pilih dulu center (try pakai 2d array utk latitude dan longitude)
#greedy algorithm