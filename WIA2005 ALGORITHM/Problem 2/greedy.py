import csv
import random
import sys
import folium
import folium.plugins as plugins
import geopy.distance
import numpy as np
import pandas as pd


class GreedyAlgorithm:
    
    def __init__(self,name,code,latBase,lngBase):
        self.name = name
        self.code = code
        self.latBase = latBase
        self.lngBase = lngBase
        self.stores = [0]*6
        self.distanceMatrix = [[0 for i in range(6)] for j in range(6)]
        self.route = [0]*len(self.distanceMatrix)
        self.countryStores = []
        self.MAX_VALUE = sys.float_info.max    
    

    def storeData(self):
        df = pd.read_csv("starbucks.csv")
        self.name = df.loc[df['state']==self.code]
        self.name = self.name.reset_index()
        self.name.to_csv(self.code+'_starbucks.csv')

        while(True):
            with open(self.code+'_starbucks.csv','r') as data:
                for row in csv.DictReader(data):
                    self.countryStores.append(row)
            break

        self.stores = random.sample(self.countryStores,k=6)


    def setDistanceMatrix(self):
        for i in range (len(self.stores)):
            for j in range (len(self.stores)):
                coordinate1 = ((self.stores[i]['latitude']),(self.stores[i]['longitude']))
                coordinate2 = ((self.stores[j]['latitude']),(self.stores[j]['longitude']))
                
                self.distanceMatrix[i][j] = geopy.distance.distance(coordinate1,coordinate2).km
                self.distanceMatrix[j][i] = geopy.distance.distance(coordinate1,coordinate2).km


    def greedyAlgorithm(self):
        index = 0
        totalCost = 0
        minCost = self.MAX_VALUE
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
        
        # 
        x = self.route[index]
        for y in range (len(self.distanceMatrix)):
            if (x!=y) and self.distanceMatrix[x][y] < minCost:
                minCost = self.distanceMatrix[x][y]

        totalCost += minCost
        print("The total travelling cost: %.4f KM" % totalCost)


    def display(self):

        # Display route sequence and total cost
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

        lat = [float(x) for x in latList if x!=0]
        lat.insert(0,float(self.stores[0]['latitude']))
        longi = [float(x) for x in lngList if x!=0]
        longi.insert(0,float(self.stores[0]['longitude']))

        waypoints = np.array(list(zip(lat,longi)))

        #create base map
        m = folium.Map(location=[self.latBase,self.lngBase],tiles="OpenStreetMap",zoom_start= 5)

        for i in range(len(self.stores)):
            lat = self.stores[i]['latitude']
            lng = self.stores[i]['longitude']

            popup = self.stores[i]['name'] + '<br>' + str(self.stores[i]['street_address']) + '<br>' + str(self.stores[i]['zip_code']) + '<br>' + str(self.stores[i]['city']) 

            folium.Marker(location=[lat,lng],popup=popup,icon=folium.Icon(color='blue')).add_to(m)
               
        plugins.AntPath(waypoints).add_to(m)
        m.save('C:\\Users\\Acer\\Documents\\SEM2-YEAR2\\WIA2005\\Assignment 1\\Problem 2\\' + self.code +'_map.html')
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Indonesia = GreedyAlgorithm('Indonesia','ID',0.7893,113.9213)
print('\nCountry:',Indonesia.name,'\n')
Indonesia.storeData()
Indonesia.setDistanceMatrix()
Indonesia.greedyAlgorithm()
Indonesia.display()


Canada = GreedyAlgorithm('Canada','CA',56.0,-96.0)
print('\nCountry:',Canada.name,'\n')
Canada.storeData()
Canada.setDistanceMatrix()
Canada.greedyAlgorithm()
Canada.display()


Malaysia = GreedyAlgorithm('Malaysia','MY',4.140634,109.6181485)
print('\nCountry:',Malaysia.name,'\n')
Malaysia.storeData()
Malaysia.setDistanceMatrix()
Malaysia.greedyAlgorithm()
Malaysia.display()


America = GreedyAlgorithm('USA','US',37.6,-95.665)
print('\nCountry:',America.name,'\n')
America.storeData()
America.setDistanceMatrix()
America.greedyAlgorithm()
America.display()


Singapore = GreedyAlgorithm('Singapore','SG',1.3146631,103.8454093)
print('\nCountry:',Singapore.name,'\n')
Singapore.storeData()
Singapore.setDistanceMatrix()
Singapore.greedyAlgorithm()
Singapore.display()