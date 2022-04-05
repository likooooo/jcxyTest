'''
Description: 
Version: 1.0
Autor: like
Date: 2022-04-05 10:46:54
LastEditors: like
LastEditTime: 2022-04-05 20:16:19
'''
import os
import re
import glob
import sys
import shutil
from textwrap import indent
from typing import Literal
from decomposeChoiceData import *
# TODO: 中文路径乱码问题

dbName = './jcxytest.csv'
tempdbName = './jcxytest_temp.csv'
dbEncode = 'utf-8'
questions = {}
questionAnsers = {}
rightAnsers = {}
commitAnswers = {}

def CreateDB():
    shutil.copyfile('./dbhistory/0.csv', dbName)
    print("Create db sucess")

def GrowthDB():
    # backup
    if not os.path.exists(tempdbName):
        shutil.copyfile(dbName, tempdbName)
    elif os.path.getsize(tempdbName) <=  os.path.getsize(dbName):
        shutil.copyfile(dbName, tempdbName)
    else:
        print("canary assert")
        return
    # read db
    
    f = open(tempdbName, 'r+',encoding = dbEncode)
    lines = f.readlines()
    for i in range(len(questions)):
        containsQuestion = False
        for j in range(0, len(lines), 5):
            if lines[j] in questions[i]:
                containsQuestion =True   
                break
        if not containsQuestion:
            a = {
                "questions" : questions[i],
                "answer": rightAnsers[i],
                "answer list" : 
                {
                    "A" : questionAnsers[i * 4], 
                    "B" : questionAnsers[i * 4 + 1], 
                    "C" : questionAnsers[i * 4 + 2], 
                    "D" : questionAnsers[i * 4 + 3]
                }
            } 
            f.write("%s\n%s\n    A:%s\n    B:%s\n    C:%s\n    D:%s\n"%(
                a['questions'], 
                a['answer'], 
                a['answer list']['A'], 
                a['answer list']['B'], 
                a['answer list']['C'], 
                a['answer list']['D']))
            print("db growth :", a)
    f.close()
    
    # backup to db
    if os.path.getsize(tempdbName) >  os.path.getsize(dbName):
        os.popen('copy %s %s'%(tempdbName, dbName))
        shutil.copyfile(tempdbName, dbName)
    return
    
    growthCount = 0
    f = open(tempdbName, encoding = dbEncode)
    for i in range(len(questions)):
        contains = False
        for j in range(len(dicts)):
            # print(dicts[j]['questions'])
            if dicts[j]["questions"] in questions[i]:
                contains =True
                j = len(dicts) - 1
        if not contains:
            a = {
            "questions" : questions[i],
            "answer": rightAnsers[i],
            "answer list" : {
                "A" : questionAnsers[i * 4], 
                "B" : questionAnsers[i * 4 + 1], 
                "C" : questionAnsers[i * 4 + 2], 
                "D" : questionAnsers[i * 4 + 3]
                }
            }  
            dicts.append(a) 
            growthCount = growthCount + 1
            print(len(dicts) ,"db growth :", a)
    f.close()
    print("db total count %d , db growth %d"%(len(dicts), growthCount))

    # save to temp db
    f = open(tempdbName, 'w', encoding = dbEncode)
    for i in range(len(dicts)):
        f.write("%s,%s,%s,%s,%s,%s\n"%(
            dicts[i]['questions'], 
            dicts[i]['answer'], 
            dicts[i]['answer list']['A'], 
            dicts[i]['answer list']['B'], 
            dicts[i]['answer list']['C'], 
            dicts[i]['answer list']['D']))
    f.close()
    
    # backup to db
    if os.path.getsize(tempdbName) >  os.path.getsize(dbName):
        os.popen('copy %s %s'%(tempdbName, dbName))


# main 
if not 2 == len(sys.argv):
    print("error format : python.exe .\dbgrowth.py 1[./1/考试结果 - 精测学院.html]")
else:
    questions, questionAnsers, rightAnsers, commitAnswers = DecomposeChoiceData('%s/考试结果 - 精测学院.html'%(sys.argv[1]))
    CheckDecompose(questions, questionAnsers, rightAnsers, commitAnswers, './dbhistory/%s.row'%(sys.argv[1]))
    files = os.listdir("./dbhistory")
    print(files)
    db = []
    for i in range(len(files)):
        print("-------------------------------\n", "./dbhistory/%s"%(files[i]))
        dict = ReadFromFile("./dbhistory/%s"%(files[i]))
        print("dbhistory : ", len(dict))
        if 0 == i:
            db = dict
            continue
        for i in range(len(dict)):
            isContaine = False
            for j in range(len(db)):
                if(db[j]["questions"] == dict[i]["questions"]):
                    isContaine = True
            if not isContaine:
                db.append(dict[i])
    f = open("db.txt", 'w', encoding = currentEncoding)
    for i in range(len(db)):
        print(db[i]["questions"])
        f.write(("%s%s%s%s%s%s")%(
            db[i]["questions"], db[i]["answer"],
            db[i]["answer list"]["A"], db[i]["answer list"]["B"], db[i]["answer list"]["C"], db[i]["answer list"]["D"]))
    f.close()
    print("Total db :", len(db))