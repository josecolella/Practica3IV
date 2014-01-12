#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re


ABaws1FileIndex = "abaws1"
ABaws2FileIndex = "abaws2"
ABazure1FileIndex = "abazure1"
ABazure2FileIndex = "abazure2"
ABvagrant1FileIndex = "abvagrant1"
ABvagrant2FileIndex = "abvagrant2"

HttpPerfaws1Index = "httpPerfaws1"
HttpPerfaws2Index = "httpPerfaws2"
HttpPerfazure1Index = "httpPerfazure1"
HttpPerfazure2Index = "httpPerfazure2"
HttpPerfvagrant1Index = "httpPerfvagrant1"
HttpPerfvagrant2Index = "httpPerfvagrant2"


tupleABFileIndex = (
    ABaws1FileIndex, ABaws2FileIndex, ABazure1FileIndex, ABazure2FileIndex,
    ABvagrant1FileIndex, ABvagrant2FileIndex)

tupleHttpPerf = (HttpPerfaws1Index, HttpPerfaws2Index, HttpPerfazure1Index,
                 HttpPerfazure2Index, HttpPerfvagrant1Index, HttpPerfvagrant2Index
                 )


totalTimePerRequest = 0
numTimes = 5
for index in tupleABFileIndex:
    fo = open(index + "Result.txt", "w")
    for i in range(1, 6):
        file = index + str(i) + ".txt"
        fi = open(file)
        fStr = fi.read()
        timePerRequest = re.search(
            'Time per request:\s+(\d+\.\d+).*\n', fStr)
        if timePerRequest:
            timePerRequest = timePerRequest.group(1)
            fo.write(
                "{}: Time per Request: {}\n".format(index, timePerRequest))
    fo.close()


replyTime = 0
numTimes = 5
for index in tupleHttpPerf:
    fo = open(index + "Result.txt", "w")
    for i in range(1, 6):
        file = index + str(i) + ".txt"
        fi = open(file)
        fStr = fi.read()
        timePerRequest = re.search(
            'Reply time \[ms\]: response (\d+\.\d+).*', fStr)
        if timePerRequest:
            timePerRequest = timePerRequest.group(1)
            fo.write(
                "{}: Reply Time: {}\n".format(index, timePerRequest))
    fo.close()
