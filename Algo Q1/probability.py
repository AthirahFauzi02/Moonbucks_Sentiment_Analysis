# get data from text file
import numpy as np
import io
import pandas as pd

def BubbleSort(Probability, n):
    swapped = False
    # Traverse through all array elements
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if Probability[j] < Probability[j + 1]:
                swapped = True
                Probability[j], Probability[j + 1] = Probability[j + 1], Probability[j]
        if not swapped:
            return

sentiment = []
CountryProb = []
country=[]
output1 = []
positiveList = []
costList = []
probability1 = []

with open('Cost.txt', 'r') as data2:
    for line in data2:
        column = line.split(' ')
        cost = float(column[0])
with open('output.txt', 'r') as data:
    for line in data:
        cells = line.split(" ")
        country1 = cells[0]
        country.append(cells[0])
        positive = float(cells[5])
        positiveList.append(positive)
        costList.append(cost)
        totalPos = sum(positiveList)
        totalCost = sum(costList)
        probability = ((3/4 * positive / totalPos) + (1/4 * cost / totalCost))
        probability1.append(probability)
        CountryProb.append((country1, probability))
        sentiment.append((country1, positive, cost, probability))
        df = pd.DataFrame(sentiment, columns=["Country", "Positive Percentage", "Cost", "Probability"])

    print(df)
    arr = probability1.copy()
    BubbleSort(arr, len(arr))
    for x in range(0, len(arr)):
        arr[x]

    SortedCountry = []
    for x in range(0, len(probability1)):
        for y in range(0, len(probability1)):
            if arr[x] == probability1[y]:
                SortedCountry.append(y)

    print("\nCountries Ranking:")
    for x in range(0, len(SortedCountry)):
        print(x + 1, '->', country[SortedCountry[x]])