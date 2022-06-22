import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


class Node:
   def __init__(self):
       self.children = {}
       self.last_letter = False

#trie algorithm
class Trie:
 
    def __init__(self):
        self.root = Node()
    
    def insert(self, word):
        cur = self.root
    
        for ch in word:
            if ch not in cur.children:
                cur.children[ch] = Node()
            cur = cur.children[ch]
        cur.last_letter = True
    
    def search(self, word):
        cur = self.root
        for ch in word:
            if ch not in cur.children:
                return False
            cur = cur.children[ch]
    
        if cur.last_letter:
            return True
        else:
            return False
    
    def startwithPrefix(self, prefix):
        cur = self.root
        for ch in prefix:
            if ch not in cur.children:
                return False
            cur = cur.children[ch]
        return True

#calculate frequencies for words
class Freq:
    def frequency(country,filter):
        neg_w=open("NEGATIVE WORDS.txt") #read textfile of negative word
        T = Trie()
        for x in neg_w:
            T.insert(x)

        tr=Trie()
        pos_w= open("POSITIVE WORDS.txt") #read textfile of positive word
        for z in pos_w:
            tr.insert(z)

        st_count=0
        filt_freq=[]
        stop_words= open("STOP WORDS.txt","r") #read textfile of stop word
        stopw= stop_words.read()
        st=stopw.splitlines()

        with open(country, encoding="utf-8") as f: #read countries' article text file
            for lines in f:
                words = lines.split()
                for r in words:
                    if not r in st: #match stop word from text file and filter stop word
                        appendFile = open(filter,'a') #append words without stop word in new text file
                        appendFile.write(r+"\n") 
                        filt_freq.append(r)
                    else:
                        st_count+=1 #count frequencies of stop word
            appendFile.close()


        p_wordfreq=[]
        with open(filter) as file1: #read file of filtered text
            for line in file1:
                word1 = line.split()
                for i in word1: 
                    if tr.startwithPrefix(i):
                        p_wordfreq.append(i)
                    else:
                        break

        n_wordfreq=[]
        with open(filter) as file2:
            for line in file2:
                word2 = line.split()
                for j in word2: 
                    if T.startwithPrefix(j):
                        n_wordfreq.append(j)
                    else:
                        break

        positive = len(p_wordfreq)
        negative = len(n_wordfreq)
        neutral = (len(filt_freq) - (negative + positive))
        Ppercent = positive / (positive + negative) * 100
        Npercent = negative / (positive + negative) * 100
        NePercent = neutral / (positive + negative + neutral) * 100

        print("The total stop word in the file is: " + str(st_count))  # print all stop word in txt files
        print("Total positive word frequency: ", positive, "%.2f" % Ppercent)
        print("Total negative word frequency: ", negative, "%.2f" % Npercent)
        print("Total neutral word frequency: ", neutral)

        outputFile = open('output.txt', 'a')
        outputFile.write(country + " " + str(neutral) + " " + str(st_count) + " " + str(positive) + " " + str(negative) + " " + str("%.2f" % Ppercent) + " " + str("%.2f" % Npercent) + " " + str("%.2f" % NePercent) + "\n")
    
fr=Freq
filter=["filteredtext.txt","filteredtext1.txt","filteredtext2.txt","filteredtext3.txt","filteredtext4.txt"]
line=["canada.txt","indonesia.txt","malaysia.txt","singapore.txt","us.txt"]
for x in filter:
    f = open(x, 'r+')
    f.truncate(0)

g = open('output.txt', 'r+')
g.truncate(0)

for i in range (5):
    print("\nCountry:", line[0])
    fr.frequency(line.pop(0),filter.pop(0))

# get data from text file
with open('output.txt', 'r') as data:
    country = []
    neutral= []
    stopWord = []
    positive = []
    negative = []
    positiveW = []
    negativeW = []
    neutralW = []

    for line in data:
        column = line.split(' ')
        country.append(column[0])
        neutral.append(float(column[1]))
        stopWord.append(float(column[2]))
        positive.append(float(column[3]))
        negative.append(float(column[4]))
        positiveW.append(float(column[5]))
        negativeW.append(float(column[6]))

    #graph for word counts
    fig1 = go.Figure(data=[
        go.Bar(name='Neutral Words', x=country, y=neutral),
        go.Bar(name='Stop Words', x=country, y=stopWord),
        go.Bar(name='Positive Words', x=country, y=positive),
        go.Bar(name='Negative', x=country, y=negative)
    ])
    # Change the bar mode
    fig1.update_layout(barmode='group')
    fig1.write_html('Word Counts Graph.html', auto_open=True)

    #graph for percentage
    fig = go.Figure(data=[
        go.Bar(name='Positive Word Percentage', x=country, y=positiveW),
        go.Bar(name='Negative Word Percentage', x=country, y=negativeW)
    ])
    # Change the bar mode
    fig.update_layout(barmode='group')
    fig.write_html('Bar Graph.html', auto_open=True)

    print("\n")
    # conclusion
    print("Summary from the Analysis in Percentage (%)")
    a = {'Country': country, 'Positive Words': positiveW, 'Negative Words': negativeW}
    df = pd.DataFrame(a)
    condition = [df['Positive Words'] > df['Negative Words'], df['Positive Words'] < df['Negative Words']]
    choice = ['Positive Sentiment', 'Negative Sentiment']
    df['Sentiment'] = np.select(condition, choice)
    print(df)

    maxPercent = max(positiveW)
    print("Based on the result, it can be concluded that article about Singapore"
          "\nhas the highest percentage of positive words which is" + " " + str(maxPercent))

"""
    inputSize = len(positiveW)
    gap = inputSize//2
    while gap>0:
        for i in range(gap, inputSize):
            temp = positiveW[i]
            j=i
            while j>=gap and positiveW[j-gap]<temp:
                positiveW[j]=positiveW[j-gap]
                j-=gap
            positiveW[j]=temp
        gap = gap//2
    print(positiveW)
"""
"""
#plot graph
values = [neutral, stopWord, positive, negative]
fig3 = px.line(x = country, y = values, labels={
                 "x": "Country", "value": "Word Count", "variable":"Types of word", "wide_variable_0":"Neutral"
             }
              ,title = "Words count")
fig3.write_html('Line Graph.html', auto_open=True)
"""