import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import plotly.offline


class Node:
   def __init__(self):
       self.children = {}
       self.last_letter = False
 
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

class Freq:
    def frequency(country,filter):
        neg_w=open("NEGATIVE WORDS.txt")
        T = Trie()
        for x in neg_w:
            T.insert(x)

        tr=Trie()
        pos_w= open("POSITIVE WORDS.txt")
        for z in pos_w:
            tr.insert(z)

        st_count=0
        filt_freq=[]
        stop_words= open("STOP WORDS.txt","r")
        stopw= stop_words.read()
        st=stopw.splitlines()
        with open(country, encoding="utf-8") as f:
            for lines in f:
                words = lines.split()
                for r in words: 
                    if not r in st: 
                        appendFile = open(filter,'a') 
                        appendFile.write(r+"\n") 
                        filt_freq.append(r)
                    else:
                        st_count+=1
            appendFile.close()


        p_wordfreq=[]
        with open(filter) as file1:
            for line in file1:
                word1 = line.split()
                for i in word1: 
                    if tr.startwithPrefix(i):
                        p_wordfreq.append(i)
                        # print(wordfreq)
                    else:
                        break

        n_wordfreq=[]
        with open(filter) as file2:
            for line in file2:
                word2 = line.split()
                for j in word2: 
                    if T.startwithPrefix(j):
                        n_wordfreq.append(j)
                        # print(wordfreq)
                    else:
                        break

        positive = len(p_wordfreq)
        negative = len(n_wordfreq)
        neutral = (len(filt_freq) - (negative + positive))
        Ppercent = positive / (positive + negative) * 100
        Npercent = negative / (positive + negative) * 100
        NePercent = neutral / (positive + negative + neutral) * 100

        #StWordPercent = (st_count / (positive + negative + neutral + st_count)) * 100
        #NeutWordPercent = (neutral / (positive + negative + neutral + st_count)) * 100
        #PosWordPercent = (positive / (positive + negative + neutral + st_count)) * 100
        #NegWordPercent = (negative / (positive + negative + neutral + st_count)) * 100

        print("The total stop word in the file is: " + str(st_count))  # print all stop word in txt files
        print("Total positive word frequency: ", positive, "%.2f" % Ppercent)
        print("Total negative word frequency: ", negative, "%.2f" % Npercent)
        print("Total neutral word frequency: ", neutral)

        outputFile = open('output.txt', 'a')
        outputFile.write(str(neutral) + " " + str(st_count) + " " + str(positive) + " " + str(negative) + " " + str("%.2f" % Ppercent) + " " + str("%.2f" % Npercent) + " " + str("%.2f" % NePercent) + "\n")
    
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
    neutral= []
    stopWord = []
    positive = []
    negative = []
    positiveW = []
    negativeW = []
    neutralW = []

    for line in data:
        column = line.split(' ')
        neutral.append(float(column[0]))
        stopWord.append(float(column[1]))
        positive.append(float(column[2]))
        negative.append(float(column[3]))
        positiveW.append(float(column[4]))
        negativeW.append(float(column[5]))
        # neutralW.append(float(column[2]))
     #plot graph
    Country = ["Canada", "Indonesia", "Malaysia", "Singapore", "US"]
    #values = [[neutral], [stopWord], [positive], [negative]]
    #fig = px.line(y=values)
    #fig.show()
    #fig = go.Figure(data=go.Scatter(y=values))
    #fig.show()

    # first plot with X and Y data
    plt.plot(Country, neutral, label = "Neutral words")
    plt.plot(Country, stopWord, label = "Stop words")
    plt.plot(Country, positive, label = "Positive words")
    plt.plot(Country, negative, label = "Negative words")

    plt.xlabel("Country")
    plt.ylabel("Words Count")
    #plt.title('multiple plots')
    plt.legend(loc="best")
    plt.show()

    x_axis = np.arange(len(Country))
    width1 = 0.2
    # plt.bar(x_axis, neutralW, width=0.2, label='Neutral Value')

    plt.bar(x_axis - width1, positiveW, width=0.4, label='Positive Value')
    plt.bar(x_axis + width1, negativeW, width=0.4, label='Negative Value')

    plt.xticks(x_axis, Country)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
               fancybox=True, shadow=True, ncol=5)
    plt.show()
    print("\n")
    # conclusion
    print("Summary from the Analysis in Percentage (%)")
    a = {'Country': Country, 'Positive Words': positiveW, 'Negative Words': negativeW}
    df = pd.DataFrame(a)
    condition = [df['Positive Words'] > df['Negative Words'], df['Positive Words'] < df['Negative Words']]
    choice = ['Positive Sentiment', 'Negative Sentiment']
    df['Sentiment'] = np.select(condition, choice)
    print(df)

    maxPercent = max(positiveW)
    print("Based on the result, it can be concluded that article about Singapore"
          "\nhas the highest percentage of positive words which is " + str(maxPercent))