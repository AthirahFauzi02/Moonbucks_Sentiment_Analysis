# get data from text file
import numpy as np
import io
import pandas as pd

def ShellSort(A, n):
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = A[i]
            j = i
            while j >= gap and A[j - gap] < temp:
                A[j] = A[j - gap]
                j -= gap
            A[j] = temp
        gap = gap // 2

sentiment = []
CountryProb = []
country=[]
output1 = []
positiveList = []
costList = []
probability1 = []
with open('output.txt', 'r') as data:
    for line in data:
        cells = line.split(" ")
        country1 = cells[0]
        country.append(cells[0])
        positive = float(cells[5])
        cost = float(cells[8])
        positiveList.append(positive)
        costList.append(cost)
        totalPos = sum(positiveList)
        totalCost = sum(costList)
        probability = ((3/4 * positive / totalPos) + (1/4 * cost / totalCost))
        probability1.append(probability)
        CountryProb.append((country1, probability))
        sentiment.append((country1, positive, cost, probability))
        df = pd.DataFrame(sentiment, columns=["Country", "Positive Percentage", "Cost", "Probability"])
        #probability[:] = [float(sentiment)]
        #ShellSort(probability, 5)
        #sort = df.sort_values(by = "Probability", ascending= False)
    print(df)
    arr = probability1.copy()
    ShellSort(arr, len(arr))
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