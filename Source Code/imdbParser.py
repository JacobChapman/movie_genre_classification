
import string
import sys
import pickle
import collections
import time
from operator import itemgetter

filename = sys.argv[1]
# keywordsFilename = sys.argv[2]
# plotFilename = sys.argv[3]
# quotesFilename = sys.argv[4]
# miscellaneousFilename = sys.argv[5]

seperator = "-------------------------------------------------------------------------------"

excludedTags = ["(V)", "(VG)", "(TV)"]

# Storage Format:
# MOVIE: [Genre 1, Genre 2, ..., Genre N]

# moves = pickle.load(open("genreData.p", "rb"))
# print("Pickle Loaded!")

file = open(filename)
entry = []
prev = ""
baddies = 0
total = 0
entryLine = file.readline()
while entryLine != "":
    entry.append(entryLine[:entryLine.__len__()-1])
    prev = entryLine
    try:
        total += 1
        entryLine = file.readline()
    except:
        baddies += 1
        # while entry[entry.__len__() - 1] != seperator:
        #     entry.pop(entry.__len__() - 1)
        # entry.pop(entry.__len__() - 1)
        # keepGoing = True
        # while keepGoing:
        #     try:
        #         keepGoing = False
        #         total += 1
        #         entryLine = file.readline()
        #     except:
        #         baddies += 1
        #         keepGoing = True
        # while entryLine != "" and entryLine[0] != '-':
        #     keepGoing = True
        #     while keepGoing:
        #         try:
        #             keepGoing = False
        #             total += 1
        #             entryLine = file.readline()
        #         except:
        #             baddies += 1
        #             keepGoing = True
file.close()
print(float(baddies / total))
numHit = 0
while numHit < 2:
    if entry[0] == seperator:
        numHit += 1
        entry.pop(0)
    else:
        entry.pop(0)

synopsisDictionary = {}

j = 0
trainTitles = []
testTitles = []

stopFile = open("datasets/stopwords.txt", "r")

stopFileLines = stopFile.readlines()
stopWords = []
for k in stopFileLines:
    stopWords.append(k.strip())
stopWords.append('')

print("Loaded stopwords!")

genreFile = open("genreData.p", 'rb')
genreData = pickle.load(genreFile)
genreFile.close()

print("Starting parse.")

start = time.time()

i = 0
while i < entry.__len__():
    # start on the first line after the "-----"
    if entry[i] != seperator and entry[i].__len__() > 3 and entry[i][:3] == "MV:":
        title = entry[i][4:]
        j+=1

        applicable = title[0] != '"' and title[title.__len__() - 4:] != "(VG)" and  title[title.__len__() - 4:] != "(TV)" \
                and title[title.__len__() - 3:] != "(V)" and "Short" not in genreData.get(title, [])

        while entry[i] != seperator and i < entry.__len__()-1:
            if applicable:
                synopsi = []

                synopsi_culled = []

                if entry[i][:3] == "PL:":
                    synopsi = entry[i][3:].split()

                    # For each element in synopsi,
                    # 1. Check for stopword, if so, remove entry
                    # 2. Strip punctuation
                    # 3. Remove capitalization
                    # Add entry to synopsi_culled

                    for sh in synopsi:
                        n = sh.translate(str.maketrans("", "", string.punctuation)).lower()

                        if n not in stopWords:
                            synopsi_culled.append(n)

                    # Handles cases where the entire line is nothing BUT stopwords
                    if synopsi_culled.__len__() != 0:
                        if title not in synopsisDictionary.keys():
                            # synopsisDictionary[title] = synopsi
                            synopsisDictionary[title] = synopsi_culled
                        else:
                            # synopsisDictionary[title].extend(synopsi)
                            synopsisDictionary[title].extend(synopsi_culled)
            i += 1
    i += 1

print("Synopses processed!")

finish = time.time()

dt = int((finish - start) * 1000)
print("Time taken to parse: " + str(dt / 1000) + " seconds.")

print("Starting dictionary build.")
start = time.time()

totalDict = []
for m in synopsisDictionary.keys():
    totalDict.extend(synopsisDictionary[m])

# Build a 2500 entry dictionary out of the word list
counter = collections.Counter(totalDict)
dictList = list(reversed(sorted(counter.items(), key=itemgetter(1))))
n = len(dictList)
for i in range(n-3500):
    dictList.pop(n-(i+1))
totalDict = []
for w in dictList:
    totalDict.append(w[0])

for m in synopsisDictionary.keys():
    length = synopsisDictionary[m].__len__()
    for i in range(length):
        if synopsisDictionary[m][length - i - 1] not in totalDict:
            synopsisDictionary[m].pop(length - i - 1)

print("Dictionary building completed in", str(int((time.time() - start))), "seconds.")

outFile = open("synopsisParse.p", 'wb')
pickle.dump(synopsisDictionary, outFile)
outFile.close()