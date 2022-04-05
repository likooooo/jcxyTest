'''
Description: 
Version: 1.0
Autor: like
Date: 2022-04-05 14:18:23
LastEditors: like
LastEditTime: 2022-04-05 21:06:55
'''
from bs4 import BeautifulSoup 
from decomposeChoiceData import * 
currentEncoding = 'utf-8'


questions     = {}
questionAnsers= {} 
answer        = {}
soup = BeautifulSoup(open('test/用户考试 - 精测学院.html', encoding=currentEncoding),features='html.parser')
# questions
temp = soup.select('div > div > div > div > ul > li > div > div > div')
for i in range(len(temp)):
    if 1 == len(temp[i]) and  'style' in temp[i].attrs.keys():  
        # print(temp[i].contents[0])
        questions[len(questions)] = temp[i].contents[0].strip()
# answers
temp = soup.select('div > div > div > div > ul > li > div > div > ul')
for i in range(len(temp)):
    if 7 == len(temp[i]):
        span = temp[i].find_all('span')
        questionAnsers[len(questionAnsers)] = str(temp[i].find_all('span')[0].contents[0])
        questionAnsers[len(questionAnsers)] = str(temp[i].find_all('span')[1].contents[0])
        questionAnsers[len(questionAnsers)] = str(temp[i].find_all('span')[2].contents[0])
        questionAnsers[len(questionAnsers)] = "\n"    
        # print("########", temp[i].find_all('span'))
    elif 9 == len(temp[i]):
        span = temp[i].find_all('span')
        questionAnsers[len(questionAnsers)] = str(temp[i].find_all('span')[0].contents[0])
        questionAnsers[len(questionAnsers)] = str(temp[i].find_all('span')[1].contents[0])
        questionAnsers[len(questionAnsers)] = str(temp[i].find_all('span')[2].contents[0])
        questionAnsers[len(questionAnsers)] = str(temp[i].find_all('span')[3].contents[0])
        # print("--------", temp[i].find_all('span'))
print(len(questions), len(questionAnsers))
for i in range(len(questions)):
    print(questions[i])
    print("    ", questionAnsers[4 * i])
    print("    ", questionAnsers[4 * i + 1])
    print("    ", questionAnsers[4 * i + 2])
    print("    ", questionAnsers[4 * i + 3])

db = ReadFromFile("./db.txt")
# print(len(db))

matchCount = 0
choices = []
hehe = []
print(len(questions))
for i in range(len(questions)):
    for j in range(len(db)):
        if questions[i] in db[j]["questions"]:
            abcd = ""
            print("##", questionAnsers[i * 4] )
            if questionAnsers[i * 4] in db[j]["answer"]:
                abcd = "A"
            elif questionAnsers[i * 4 + 1] in db[j]["answer"]:
                abcd = "B"
            elif questionAnsers[i * 4 + 2] in db[j]["answer"]:
                abcd = "C"
            elif questionAnsers[i * 4 + 3] in db[j]["answer"]:
                abcd = "D"
            else:
                abcd = "None"
            hehe.append(abcd)
            choices.append(("%s( Suggest %s)")%(db[j]["answer"][2:], abcd))
            matchCount = matchCount + 1
            break
        if j == len(db) - 1:
            choices.append("No db matched")
            hehe.append("None")
            
for i in range(len(choices)):
    print(i + 1, choices[i])
    print( i + 1, hehe[i])
print("预测分数 : ", matchCount * 2)
if 90 > matchCount * 2:
    print("不用做了, 数据库不充足 , match count", matchCount)
    raise Exception("db not strong")

