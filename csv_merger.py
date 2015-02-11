#!/usr/bin/env python
# -*- coding: utf-8 -*-

# problems: XPCLG-17BB
# semi problem: AFN2-36GT
# semi problem 2: VWV-P092
# semi problem 3: MVWV-P112 (gibts auch)
# XPCLT-17SB gibt es garnicht

# FIXME!! VWV-P112\x89

preStringList = ["S", "B"]

import csv
import sys
goodList = []
keyList = []
dataDict = {}
finalDict = {}


# helper
def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]

# main methods
print "Reading from: %s" % sys.argv[1]
with open(sys.argv[1], 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')

    count = 0
    firstGoodCount = 0

    # string of all chars
    a = ''.join([chr(n) for n in range(256)])
    # string of wanted chars
    b = ''.join([n for n in a if ord(n) >= 32 and ord(n) <= 126])
    # string of unwanted chars > ord(126)
    c = ''.join([n for n in a if ord(n) < 32 or ord(n) > 126])

    for row in reader:
        count += 1

        row0 = "".join([("" if n in c else n) for n in row[0] if n not in c]).strip()
        row1 = "".join([("" if n in c else n) for n in row[1] if n not in c]).strip()
        row2 = "".join([("" if n in c else n) for n in row[2] if n not in c]).strip()

        if row0:
            firstGoodCount += 1
            goodList.append(row0)

        if row1 and row2:
            keyList.append(row1)
            dataDict[row1] = row2

    goodList = f7(goodList)
    goodCount = len(goodList)

    print "Lines: %s, good count: %s (%s)" % (count, goodCount, firstGoodCount)

resName = sys.argv[1].replace('.csv', '') + "_result.csv"
print "Writing to: %s" % resName
with open(resName, 'wb') as f:
    identCount = 0
    guessedCount = 0
    missingCount = 0
    missingList = []
    duplicatedCount = 0
    guessedList = []
    preStringCount = 0
    searchMe = "GP-16G"

    writer = csv.writer(f)
    for testKey in goodList:
        if testKey in keyList:
            # absolut identisch
            identCount += 1
            writer.writerow([testKey, dataDict[testKey]])

        else:
            foundList = []

            for key in keyList:
                if testKey in key:
                    foundList.append(key)

            # nich gefunden
            if len(foundList) == 0:
                missingCount += 1
                missingList.append(testKey)
                writer.writerow([testKey, "?"])
                # print "No matching key found for: %s" % testKey

            # kommt vor
            elif len(foundList) == 1:
                identCount += 1
                # print "Found one single match, guessing: %s > %s" % (testKey, foundList[0])
                writer.writerow([testKey, dataDict[foundList[0]]])

            # mehrfache gefunden
            else:

                withoutPoint = False
                foundWithPreString = False
                for item in foundList:
                    allPreStringsFound = True
                    for preString in preStringList:
                        foundString = "%s%s" % (preString, testKey)
                        if foundString not in foundList:
                            allPreStringsFound = False

                    if allPreStringsFound:
                        foundWithPreString = True
                        preStringCount += 1
                        for preString in preStringList:
                            foundString = "%s%s" % (preString, testKey)
                            writer.writerow([foundString, dataDict[foundString]])

                    if foundWithPreString:
                        break

                    if "." not in item:
                        withoutPoint = True

                if foundWithPreString:
                    pass

                elif not withoutPoint:
                    # brav
                    guessedCount += 1
                    writer.writerow([testKey, dataDict[foundList[-1]]])
                else:
                    print "Found multiple matches for: %s (%s)" % (testKey, ', '.join(foundList))
                    writer.writerow([testKey, "???"])
                    guessedList.append(testKey)
                    duplicatedCount += 1

    print "Number of keys: %s" % len(keyList)
    print "Good (%s)\t%s identical, %s guessed and pre string %s" % ((identCount + guessedCount + preStringCount), identCount, guessedCount, preStringCount)
    print "Bad (%s)\t%s missing and %s duplicates" % ((missingCount + duplicatedCount), missingCount, duplicatedCount)
    totalLines = missingCount + identCount + guessedCount + duplicatedCount + preStringCount
    if goodCount != totalLines:
        print "Something is wrong! Wrong amount of lines"
    # print "Duplicates found List:\n%s" % ' '.join(guessedList)
