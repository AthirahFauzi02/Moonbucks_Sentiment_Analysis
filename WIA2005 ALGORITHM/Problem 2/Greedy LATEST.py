import os
import sys
import folium
import folium.plugins as plugins
import geopy.distance
import numpy as np
import pandas as pd
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from scipy.cluster.vq import vq


class Problem2:
    
    def __init__(self,name,code,latBase,lngBase):
        self.name = name
        self.code = code
        self.latBase = latBase
        self.lngBase = lngBase
        self.stores = []
        self.distanceMatrix = []
        self.route = []
        self.countryStores = []
        self.MAX_VALUE = sys.float_info.max
    

    def storeData(self):
        df = pd.read_csv("starbucks.csv")
        self.countryStores = df.loc[df['state']==self.code]
        self.countryStores = self.countryStores.reset_index()
        self.countryStores.drop('index', inplace=True, axis=1)
        self.stores = self.countryStores.head(45).to_dict(orient='records')
        self.countryStores = self.countryStores.head(6)


    def kMeansAlgorithm(self):
        pd.set_option('mode.chained_assignment', None)
        
        df = self.countryStores[["latitude","longitude"]]

        km = KMeans(n_clusters=1)
        y_predicted = km.fit_predict(df[['latitude','longitude']])

        # Predicting cluster based on number of clusters
        df['cluster'] = y_predicted

        # Scalling dataset
        scaler = MinMaxScaler()

        scaler.fit(df[['latitude']])
        df['latitude'] = scaler.transform(df[['latitude']])

        scaler.fit(df[['longitude']])
        df['longitude'] = scaler.transform(df[['longitude']])

        # Re-predict centroid
        km = KMeans(n_clusters=1)
        y_predicted = km.fit_predict(df[['latitude','longitude']])

        # The final centroid
        km.cluster_centers_

        # Find the nearest point from centroid
        # 'closest' is the index of the nearest data point to centroid
        closest, distances = vq(km.cluster_centers_, df[['latitude', 'longitude']])
                
        # Swap center position
        self.stores[0],self.stores[closest[0]] = self.stores[closest[0]],self.stores[0]
        

    def setDistanceMatrix(self):
        self.distanceMatrix = [[0 for i in range(len(self.stores))] for j in range(len(self.stores))]
        for i in range (len(self.stores)):
            for j in range (len(self.stores)):
                coordinate1 = ((self.stores[i]['latitude']),(self.stores[i]['longitude']))
                coordinate2 = ((self.stores[j]['latitude']),(self.stores[j]['longitude']))
                
                self.distanceMatrix[i][j] = geopy.distance.distance(coordinate1,coordinate2).km
                self.distanceMatrix[j][i] = geopy.distance.distance(coordinate1,coordinate2).km


    def nearestNeighbourAlgorithm(self):
        index = 0
        totalCost = 0
        minCost = self.MAX_VALUE
        self.route = [0]*len(self.distanceMatrix)
        visitedStoreList = [dict() for k in range(len(self.stores))]
        visitedStoreList[0] = {'name':self.stores[0]['name'],'hasBeenVisited':'TRUE'}
        
        x,y = (0,0)
        while x < len(self.distanceMatrix) and y < len(self.distanceMatrix[x]):

            if index >= len(self.distanceMatrix[x]) - 1:
                break
            
            if y!=x and not ('TRUE' in visitedStoreList[y].values()):
                if self.distanceMatrix[x][y] < minCost:
                    minCost = self.distanceMatrix[x][y]
                    self.route[index] = y
            
            y += 1

            if y == len(self.distanceMatrix[x]):
                totalCost += minCost
                minCost = self.MAX_VALUE
                visitedStoreList[self.route[index]] = {'name':self.stores[self.route[index]]['name'],'hasBeenVisited':'TRUE'}
                y = 0
                x = self.route[index]
                index += 1
        
        x = self.route[index]
        for y in range (len(self.distanceMatrix)):
            if (x!=y) and self.distanceMatrix[x][y] < minCost:
                minCost = self.distanceMatrix[x][y]

        totalCost += minCost
        print("The total travelling cost: %.4f KM" % totalCost)
        # return totalCost


    def display(self):

        # Display route sequence
        print('\nRoute:',end=' ')
        print(self.stores[0]['name'],'->',end=' ')
        for i in range(len(self.stores)-1):
            print(self.stores[self.route[i]]['name'],'->',end=' ')
        print(self.stores[0]['name'],'\n')

        latList = [0 for i in range(len(self.stores)+1)]
        latList[0] = self.stores[0]['latitude']
        
        lngList = [0 for i in range(len(self.stores)+1)]
        lngList[0] = self.stores[0]['longitude']

        for p in range(len(self.stores)-1):
            latList.append(self.stores[self.route[p]]['latitude'])
            lngList.append(self.stores[self.route[p]]['longitude'])
        latList.append(self.stores[0]['latitude'])
        lngList.append(self.stores[0]['longitude'])

        latList = [float(i) for i in latList if i!=0]
        lngList = [float(i) for i in lngList if i!=0]

        waypoints = np.array(list(zip(latList,lngList)))

        # Display map
        m = folium.Map(location=[self.latBase,self.lngBase],tiles="OpenStreetMap",zoom_start= 5)

        for i in range(len(self.stores)):
            lat = self.stores[i]['latitude']
            lng = self.stores[i]['longitude']

            if i == 0:
                popup = self.stores[0]['name'] + '<br>' + str(self.stores[0]['street_address']) + '<br>' + str(self.stores[0]['zip_code']) + '<br>' + str(self.stores[0]['city'])  
                folium.Marker(location=[self.stores[0]['latitude'],self.stores[0]['longitude']],popup=popup,icon=folium.Icon(color='green')).add_to(m)

            else:
                popup = self.stores[i]['name'] + '<br>' + str(self.stores[i]['street_address']) + '<br>' + str(self.stores[i]['zip_code']) + '<br>' + str(self.stores[i]['city']) 
                folium.Marker(location=[lat,lng],popup=popup,icon=folium.Icon(color='blue')).add_to(m)


        plugins.AntPath(waypoints).add_to(m)
        m.save('C:\\Users\\Acer\\Documents\\GitHub\\Moonbucks-Store-Project\\Problem 2\\'+self.code+'_map.html')
        # os.system('cmd /c start chrome "C:\\Users\\Acer\\Documents\\GitHub\\Moonbucks-Store-Project\\Problem 2\\'+self.code+'_map.html"')


# totalCost = []


Indonesia = Problem2('Indonesia','ID',0.7893,113.9213)
print('\nCountry:',Indonesia.name,'\n')
Indonesia.storeData()
Indonesia.kMeansAlgorithm()
Indonesia.setDistanceMatrix()
# totalCost.append({'name':Indonesia.name,'cost':Indonesia.greedyAlgorithm()})
Indonesia.nearestNeighbourAlgorithm()
Indonesia.display()

Canada = Problem2('Canada','CA',56.0,-96.0)
print('\nCountry:',Canada.name,'\n')
Canada.storeData()
Canada.kMeansAlgorithm()
Canada.setDistanceMatrix()
# totalCost.append({'name':Canada.name,'cost':Canada.greedyAlgorithm()})
Canada.nearestNeighbourAlgorithm()
Canada.display()


Malaysia = Problem2('Malaysia','MY',4.140634,109.6181485)
print('\nCountry:',Malaysia.name,'\n')
Malaysia.storeData()
Malaysia.kMeansAlgorithm()
Malaysia.setDistanceMatrix()
# totalCost.append({'name':Malaysia.name,'cost':Malaysia.greedyAlgorithm()})
Malaysia.nearestNeighbourAlgorithm()
Malaysia.display()


America = Problem2('USA','US',37.6,-95.665)
print('\nCountry:',America.name,'\n')
America.storeData()
America.kMeansAlgorithm()
America.setDistanceMatrix()
# totalCost.append({'name':America.name,'cost':America.greedyAlgorithm()})
America.nearestNeighbourAlgorithm()
America.display()


Singapore = Problem2('Singapore','SG',1.3146631,103.8454093)
print('\nCountry:',Singapore.name,'\n')
Singapore.storeData()
Singapore.kMeansAlgorithm()
Singapore.setDistanceMatrix()
# totalCost.append({'name':Singapore.name,'cost':Singapore.greedyAlgorithm()})
Singapore.nearestNeighbourAlgorithm()
Singapore.display()


# rank = sorted(totalCost,key=lambda i: i['cost'])
# print("Country rank:\n")
# for k in range(len(rank)):
#     print(k+1,' ',rank[k]['name'])
# print('\r')
