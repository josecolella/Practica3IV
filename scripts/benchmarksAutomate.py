#!/usr/bin/env python3


import os
import sys


def generateAbBenchmarks(argument):
    for i in range(1, 6):
        if argument == "azure1":
            p = os.popen(
                "ab -n 1000 -c 100 http://ivmachine.cloudapp.net/index.html", "r")
        elif argument == "azure2":
            p = os.popen(
                "ab -n 1000 -c 100 http://ivmachine2.cloudapp.net/index.html", "r")
        elif argument == "aws1":
            p = os.popen(
                "ab -n 1000 -c 100 http://ec2-54-194-187-157.eu-west-1.compute.amazonaws.com/index.html", "r")
        elif argument == "aws2":
            p = os.popen(
                "ab -n 1000 -c 100 http://54.194.113.118/index.html", "r")
        elif argument == "vagrant1":
            p = os.popen(
                "ab -n 100 -c 10 http://127.0.0.1:8080/index.html", "r")
        elif argument == "vagrant2":
            p = os.popen(
                "ab -n 100 -c 10 http://127.0.0.1:8081/index.html", "r")
        print("Iteration: {}".format(i))
        fo = open("ab{}{}.txt".format(argument, i), "w")
        line = p.readline()
        while line != '':
            fo.write(line)
            line = p.readline()
        fo.close()


def generateHTTPPerfBenchmarks(argument):
    for i in range(1, 6):
        if argument == "azure2":
            p = os.popen(
                "httperf --server 137.117.146.8 --port 80 --rate 10 --num-conn 1000 --uri /index.html", "r")
        elif argument == "azure1":
            p = os.popen(
                "httperf --server 137.117.145.175  --port 80 --rate 10 --num-conn 1000 --uri /index.html", "r")
        elif argument == "aws1":
            p = os.popen(
                "httperf --server 54.194.187.157 --port 80 --rate 10 --num-conn 1000 --uri /index.html", "r")
        elif argument == "aws2":
            p = os.popen(
                "httperf --server 54.194.113.118 --port 80 --rate 10 --num-conn 1000 --uri /index.html", "r")
        elif argument == "vagrant1":
            p = os.popen(
                "httperf --server 127.0.0.1 --port 8080 --rate 10 --num-conn 1000 --uri /index.html", "r")
        elif argument == "vagrant2":
            p = os.popen(
                "httperf --server 127.0.0.1 --port 8081 --rate 10 --num-conn 1000 --uri /index.html", "r")
        print("Iteration: {}".format(i))
        fo = open("httpPerf{}{}.txt".format(argument, i), "w")
        line = p.readline()
        while line != '':
            fo.write(line)
            line = p.readline()
        fo.close()


if __name__ == '__main__':
    try:
        # generateAbBenchmarks(sys.argv[1])
        generateHTTPPerfBenchmarks(sys.argv[1])
    except Exception:
        print("Tiene que haber un argumento: <azure1>, <azure2>, <aws1>, <aws2>, <vagrant1>, <vagrant2>")
