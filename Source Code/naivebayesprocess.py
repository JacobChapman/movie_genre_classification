
import pickle
import math
from operator import itemgetter

synopsisFile = open("synopsisData.p", 'rb')
genreFeatures, synopsisData = pickle.load(synopsisFile)
synopsisFile.close()

genreFile = open("genreData.p", 'rb')
genreListings = pickle.load(genreFile)
genreFile.close()

testDataGenres = {}
for m in synopsisData.keys():
    testDataGenres[m] = []
for g in genreFeatures.keys():
    total = sum(genreFeatures[g].values())
    probabilities = []
    for m in synopsisData.keys():
        prob = 0
        for w in synopsisData[m]:
            prob -= math.log(float(genreFeatures[g].get(w, 0) + 1) / float(total))
        testDataGenres[m].append([g, prob])

correct = 0
correct2 = 0
total = 0
total2 = 0
for m in synopsisData.keys():
    isC = "Incorrect"
    isC2 = ":"
    testDataGenres[m] = sorted(testDataGenres[m], key=itemgetter(1))
    if testDataGenres[m][0][0] in genreListings.get(m, []):
        isC = "Correct"
        correct += 1
    if testDataGenres[m][1][0] in genreListings.get(m, []):
        isC2 = "(Second): "
        correct2 += 1
    exists = False
    onFirst = True
    for g in genreListings.get(m, []):
        if g in genreFeatures.keys():
            if onFirst:
                total += 1
                exists = True
                onFirst = False
            else:
                total2 += 1
                break
    #if exists:
    #    print(isC, isC2, m, ":", testDataGenres[m][0][0], testDataGenres[m][1][0])

print("Percentage correct: ", str((correct / total) * 100))
print("Secondaries correct: ", str((correct2 / total) * 100))

print(testDataGenres["Love N' Dancing (2009)"])