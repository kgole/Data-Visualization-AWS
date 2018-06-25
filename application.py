#https://github.com/altmanWang/IBM-DB2/blob/master/Insert.py
import csv
from numpy import vstack,array
import os
from scipy.cluster.vq import kmeans,vq
from flask import Flask, render_template, request
import collections
import pymysql
import plotly.plotly as py
import plotly.graph_objs as go
import plotly
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pyplot
import io


cnxn = pymysql.connect()
cursor = cnxn.cursor()

plotly.plotly.sign_in()
application = Flask(__name__)



@application.route('/')
def index():
    return render_template('index.html')

@application.route('/upload', methods=['POST', 'GET'])
def graph():
    if request.method == 'POST':
        x='age'
        y='fare'
        k=8

        sample = []
        f = csv.reader(open('titanic3.csv', "r"), delimiter=",")
        headers = next(f)
        x = headers.index(x)
        y = headers.index(y)
        count = 0
        next(f, None)
        for row in f:
            value = []
            if row[x] != '' and row[y] != '':
                value.append(float(row[x]))
                value.append(float(row[y]))
                sample.append(value)
                count = count + 1

        data = vstack(sample)
        result=[]
        centroids, _ = kmeans(sample, k)
        print(_)
        print(centroids)
        idx, _ = vq(data, centroids)
        label = collections.Counter(idx)
        print(label)

        mark = ['o']

        for i in range(0, k):
            pyplot.plot(data[idx == i, 0], data[idx == i, 1], marker=mark[0], ls='none')
        pyplot.plot(centroids[:, 0], centroids[:, 1], 'sm', markersize=8)

        pyplot.savefig('static/output.png')

    return render_template('scatter.html', centroids=centroids)


@application.route('/barchartmale', methods=['POST', 'GET'])
def barchart1():
    if request.method == 'POST':
        query1 = "select count(*) from titanic where sex='male' group by pclass"
        cursor.execute(query1)
        rowdata=[]
    for row in cursor:

        rowdata.append(row)

    print(rowdata)
    data = [go.Bar(
        x=['Class A', 'Class B', 'Class C'],
        y=(rowdata)
    )]
    py.plot(data, filename='basic-bar')

    return render_template('barlink.html')

@application.route('/piechartmale', methods=['POST', 'GET'])
def piechart1():
    if request.method == 'POST':
        query1 = "select count(*) from titanic where sex='male' group by pclass"
        cursor.execute(query1)
        rowdata=[]
    for row in cursor:

        rowdata.append(row)

    print(rowdata)
    x=['Class A', 'Class B', 'Class C']
    y=(rowdata)

    trace = go.Pie(labels=x, values=y)

    py.plot([trace], filename='basic_pie_chart')
    return render_template('pielink.html')


@application.route('/barchartfemale', methods=['POST', 'GET'])
def barchart2():
    if request.method == 'POST':
        query1 = "select count(*) from titanic where sex='female' group by pclass"
        cursor.execute(query1)
        rowdata=[]
    for row in cursor:

        rowdata.append(row)

    print(rowdata)
    data = [go.Bar(
        x=['Class A', 'Class B', 'Class C'],
        y=(rowdata)
    )]
    py.plot(data, filename='basic-bar')

    return render_template('barlink.html')

@application.route('/piechartfemale', methods=['POST', 'GET'])
def piechart2():
    if request.method == 'POST':
        query1 = "select count(*) from titanic where sex='female' group by pclass"
        cursor.execute(query1)
        rowdata=[]
    for row in cursor:

        rowdata.append(row)

    print(rowdata)
    x=['Class A', 'Class B', 'Class C']
    y=(rowdata)

    trace = go.Pie(labels=x, values=y)

    py.plot([trace], filename='basic_pie_chart')
    return render_template('pielink.html')



if __name__ == '__main__':
    application.run(debug = True)

