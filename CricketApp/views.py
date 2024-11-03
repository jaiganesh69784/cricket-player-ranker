from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
import pymysql
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from hmmlearn import hmm
import operator
import pickle

global username

def Batsman(request):
    if request.method == 'GET':
        global uname
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Player No</font></th>'
        output+='<th><font size=3 color=black>Player Name</font></th>'
        output+='<th><font size=3 color=black>Performance Accuracy</font></th></tr>'
        dataset = pd.read_csv("Dataset/bat.csv", usecols = ['name_x', 'runs_x', 'balls', 'strike_rate', 'fours', 'sixes', 'how_out', 'run_rate'])
        le1 = LabelEncoder()
        le2 = LabelEncoder()
        scaler = StandardScaler()
        dataset['name_x'] = pd.Series(le1.fit_transform(dataset['name_x'].astype(str)))
        dataset['how_out'] = pd.Series(le2.fit_transform(dataset['how_out'].astype(str)))
        dataset = dataset.values
        X = dataset[:,0:dataset.shape[1]-1]
        Y = dataset[:,dataset.shape[1]-1]
        X = scaler.fit_transform(X)
        print(X.shape)
        print(Y.shape)
        if os.path.exists("model/bat"):
            with open('model/bat', 'rb') as file:
                model = pickle.load(file)
            file.close()
        else:
            model = hmm.GaussianHMM(10, "full", n_iter=500)
            model.fit(X)
            with open('model/bat', 'wb') as file:
                pickle.dump(model, file)
            file.close()
        testData = pd.read_csv("Dataset/test_bat.csv", usecols = ['name_x', 'runs_x', 'balls', 'strike_rate', 'fours', 'sixes', 'how_out'])
        player = testData['name_x']
        testData['name_x'] = pd.Series(le1.transform(testData['name_x'].astype(str)))
        testData['how_out'] = pd.Series(le2.transform(testData['how_out'].astype(str)))
        testData = testData.values
        X = scaler.transform(testData)
        performance = []
        predict = model.predict(X)
        selected = []
        for i in range(len(predict)):
            if player[i] not in selected:
                selected.append(player[i])
                performance.append([player[i], predict[i]])
        performance.sort(key = operator.itemgetter(1), reverse = True)
        for i in range(0,15):
            player_name = performance[i][0]
            accuracy = performance[i][1]
            output+='<tr><td><font size=3 color=black>'+str(i+1)+'</font></td>'
            output+='<td><font size=3 color=black>'+str(player_name)+'</font></td>'
            output+='<td><font size=3 color=black>'+str(accuracy)+'</font></td></tr>'
        output+="</table><br/><br/><br/><br/><br/><br/>"
        context= {'data':output}
        return render(request, 'ViewPrediction.html', context)

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def UserLogin(request):
    if request.method == 'GET':
       return render(request, 'UserLogin.html', {})

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def Signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        contact = request.POST.get('contact', False)
        gender = request.POST.get('gender', False)
        email = request.POST.get('email', False)
        address = request.POST.get('address', False)
        usertype = request.POST.get('usertype', False)
        output = "Error in signup process"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'cricket',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username FROM signup")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    output = username+" Username already exists"
                    break
        if output == 'Error in signup process':
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'cricket',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO signup(username,password,contact_no,gender,email,address,usertype) VALUES('"+username+"','"+password+"','"+contact+"','"+gender+"','"+email+"','"+address+"','"+usertype+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                output = 'Signup Process Completed'
        context= {'data':output}
        return render(request, 'Register.html', context)

def UserLoginAction(request):
    if request.method == 'POST':
        global uname
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user_type = ""
        index = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'cricket',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username,password,usertype FROM signup")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and password == row[1]:
                    user_type = row[2]
                    uname = username
                    index = 1
                    break
        if index == 1:
            context= {'data':"Welcome "+uname+"<br/>You Logged in as "+user_type}
            return render(request, 'UserScreen.html', context)
        else:
            context= {'data':'login failed'}
            return render(request, 'UserLogin.html', context)

def Ballers(request):
    if request.method == 'GET':
        global uname
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Player No</font></th>'
        output+='<th><font size=3 color=black>Player Name</font></th>'
        output+='<th><font size=3 color=black>Performance Accuracy</font></th></tr>'
        #reading dataset
        dataset = pd.read_csv("Dataset/ball.csv", usecols = ['name_x', 'run_conceded', 'maidens', 'wickets', 'overs', 'economy', 'wides', 'no_balls', 'fours',
                                                     'sixes', 'zeros', 'runs', 'over', 'run_rate'])
        dataset.fillna(0, inplace = True)
        le1 = LabelEncoder()
        scaler = StandardScaler()
        dataset['name_x'] = pd.Series(le1.fit_transform(dataset['name_x'].astype(str)))
        X = dataset.values
        X = scaler.fit_transform(X)
        if os.path.exists("model/ball"):
            with open('model/ball', 'rb') as file:
                model = pickle.load(file)
            file.close()
        else:
            #now training HMM model on training dataset
            model = hmm.GaussianHMM(10, "full", n_iter=5000)
            model.fit(X)
            with open('model/ball', 'wb') as file:
                pickle.dump(model, file)
            file.close()
        testData = pd.read_csv("Dataset/test_ball.csv", usecols = ['name_x', 'run_conceded', 'maidens', 'wickets', 'overs', 'economy', 'wides',
                                                                   'no_balls', 'fours', 'sixes', 'zeros', 'runs', 'over', 'run_rate'])
        testData.fillna(0, inplace = True)
        player = testData['name_x']
        testData['name_x'] = pd.Series(le1.transform(testData['name_x'].astype(str)))
        testData = testData.values
        X = scaler.transform(testData)
        performance = []
        predict = model.predict(X)
        selected = []
        for i in range(len(predict)):
            if player[i] not in selected:
                selected.append(player[i])
                performance.append([player[i], predict[i]])
        performance.sort(key = operator.itemgetter(1), reverse = True)
        for i in range(0,15):
            player_name = performance[i][0]
            accuracy = performance[i][1]
            output+='<tr><td><font size=3 color=black>'+str(i+1)+'</font></td>'
            output+='<td><font size=3 color=black>'+str(player_name)+'</font></td>'
            output+='<td><font size=3 color=black>'+str(accuracy)+'</font></td></tr>'
        output+="</table><br/><br/><br/><br/><br/><br/>"
        context= {'data':output}
        return render(request, 'ViewPrediction.html', context)
