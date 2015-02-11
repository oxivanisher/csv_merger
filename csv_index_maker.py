#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os
import sys

dataPath = sys.argv[2]

csvData = []
txtData = {}
ignoreFiles = ['.DS_Store']

# main methods
srcName = sys.argv[1].replace('.csv', '') + "_result.csv"
print "Reading from: %s" % srcName
with open(srcName, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')

    for row in reader:
        csvData.append(row)

print "Found %s lines in csv" % len(csvData)

files =[]
for (dirpath, dirnames, filenames) in os.walk(dataPath):
    files.extend(filenames)

for fileName in files:
    if fileName not in ignoreFiles:
        page = fileName.replace('extract-', '').replace('.txt', '')
        f = open(os.path.join(dataPath, fileName), 'rb')
        txtData[page] = f.read()
        f.close()

print "Found %s pages of text" % len(txtData)

dstName = sys.argv[1].replace('.csv', '') + "_result_with_index.csv"
print "Writing to: %s" % dstName
with open(dstName, 'wb') as f:
    writer = csv.writer(f)
    count = 0
    for line in csvData:
        count += 1
        foundInPages = []
        for page in txtData.keys():
            if line[0] in txtData[page]:
                foundInPages.append(int(page))

        pageStrList = []
        for page in sorted(foundInPages):
            pageStrList.append(str(page))
        # print line + [', '.join(pageStrList)]
        writer.writerow(line + [', '.join(pageStrList)])

print "Wrote %s lines to csv" % count