'''
Description: 
Version: 1.0
Autor: like
Date: 2022-04-05 09:03:43
LastEditors: like
LastEditTime: 2022-04-05 21:46:00
'''
from bs4 import BeautifulSoup 
import json
currentEncoding = 'utf-8'


def DecomposeChoiceData(htmlPath):#'1/考试结果 - 精测学院.html'
    soup = BeautifulSoup(open(htmlPath, encoding=currentEncoding),features='html.parser')
    # 答案
    questions     = []
    questionAnsers= [] # 3 到 4 个选项 , 如果只有 3 个选项, 第四个选项就是 \n
    commitAnswers = []
    rightAnsers   = []
    # 题型入口 : div > div > div > div > h4 > div
    temp = soup.select("div > div > div > div > div > div > div > div")
    count = 4
    for i in range(len(temp)):
        if not (1 == len(temp[i]) and 'class' in temp[i].attrs):
            continue
        if 3 == len(temp[i].attrs['class']):
            for i in range(count, 4): #填充第四个选项
                questionAnsers.append("None")
                print("    ", questionAnsers[len(questionAnsers) - 1])
            count = 0
            # print('~~~~~~', temp[i].contents[0])
            questions.append(temp[i].contents[0])
            print(questions[len(questions) - 1])
        elif 6 == len(temp[i].attrs['class']):
            questionAnsers.append(temp[i].contents[0])
            print("    ", questionAnsers[len(questionAnsers) - 1])
            count = count + 1
    for i in range(count, 4): #填充第四个选项
        questionAnsers.append("None")
        print("    ", questionAnsers[len(questionAnsers) - 1])
    # print(len(questions), len(questionAnsers))
    if 50 != len(questions) or 200 != len(questionAnsers):
        raise Exception("Decompose data error")

    # 答案 
    temp = soup.select("div > div > div > div > div > div > div > h3")
    for i in range(len(temp)):
        # print("####", len(temp[i]))
        # print(temp[i])
        if 3 == len(temp[i]):
            # print("##", temp[i])
            commitAnswers.append(temp[i].contents[1][1:])
            # print(commitAnswers[len(commitAnswers) - 1])
        elif 2 == len(temp[i]):
            # print("~~~", temp[i])
            rightAnsers.append(temp[i].contents[1][1:])
            # print(rightAnsers[len(commitAnswers) - 1])
    if 50 != len(commitAnswers) or 50 != len(rightAnsers):
        raise Exception("Decompose data error")
    return [questions, questionAnsers, rightAnsers, commitAnswers]
    
#  def GetQuestionStructs(questions, questionAnsers, rightAnsers):
#     dict = []
#     for i in range(len(questions)):
#         a = {
#             "questions" : questions[i],
#             "answer": rightAnsers[i],
#             "answer list" : 
#             {
#                 "A" : questionAnsers[i * 4], 
#                 "B" : questionAnsers[i * 4 + 1], 
#                 "C" : questionAnsers[i * 4 + 2], 
#                 "D" : questionAnsers[i * 4 + 3]
#             }
#         }  
#         # print(a)
#         dict.append(a)
#     return dict   

def CreateChoiceStruct(question, rightAnser, myquestionAnser, a, b, c, d):
    str = "Error"
    if "A" == rightAnser:
        str = a
    elif "B" == rightAnser:
        str = b
    elif "C" == rightAnser:
        str = c
    elif "D" == rightAnser:
        str = d  
    answer = ("%s,%s")%(rightAnser, str)
    # print("### CreateChoiceStruct %s : %s(%s) %s/%s/%s/%s"%(question, answer, myquestionAnser, a, b, c, d))
    a = {
        "questions" : question,
        "answer": answer,
        "answer list" : 
        {
            "A" : a, 
            "B" : b, 
            "C" : c, 
            "D" : d
        }
    }  
    return a
def ToString(struct):
    return ("%s\n%s\n    %s\n    %s\n    %s\n    %s\n")%(
        struct["questions"], struct["answer"], 
        struct["answer list"]["A"], struct["answer list"]["B"], struct["answer list"]["C"], struct["answer list"]["D"]
    )
def CheckDecompose(questions, questionAnsers, rightAnsers, commitAnswers, path):
    print("right answer : ", len(rightAnsers))
    print("commit answer : ", len(commitAnswers))

    print("question count : ", len(questions))
    print("question answer count : ", len(questionAnsers))

    testscore = 0
    for i in range(len(questions)):
        print(questions[i])
        print("    ", questionAnsers[i * 4])
        print("    ", questionAnsers[i * 4 + 1])
        print("    ", questionAnsers[i * 4 + 2])
        print("    ", questionAnsers[i * 4 + 3])
        print("Right anser ", rightAnsers[i], "Your answer " , commitAnswers[i])
        if commitAnswers[i] == rightAnsers[i]:
            testscore = testscore + 2
    print("\n\nFinal score : ", testscore)

    f = open(path, 'w', encoding = currentEncoding)
    for i in range(len(questions)):
        a = CreateChoiceStruct(questions[i], rightAnsers[i], commitAnswers[i], 
        questionAnsers[4 * i], questionAnsers[4 * i + 1], questionAnsers[4 * i + 2], questionAnsers[4 * i + 3])
        f.write(ToString(a))
        print(ToString(a))
    f.close()

def ReadFromFile(path):
    f = open(path, 'r', encoding= currentEncoding)
    lines = f.readlines()
    dicts = []
    for i in range(0, len(lines), 6):
        question = lines[i]
        answer = lines[i + 1]
        print("###", question, answer, i, path)
        a = lines[i + 2]
        b = lines[i + 3]
        c = lines[i + 4]
        d = lines[i + 5]

        struct = {
            "questions" : question,
            "answer": answer,
            "answer list" : 
            {
                "A" : a, 
                "B" : b, 
                "C" : c, 
                "D" : d
            }
        }  
        dicts.append(struct)
    f.close()
    return dicts