# encoding: utf-8

import requests
import bs4 
import time
import json

#读取文件
def read_file(_file):
    with open(_file, 'r', encoding='utf-8') as infile:
        return json.load(infile)

#保存文件
def save_file(_data,_file):
    with open(_file, 'w', encoding='utf-8') as outfile:
        outfile.write(_data)


input_url = input("输入url地址:")
url = (input_url + "&pageSize=50").replace('startAnswerQuestion','getQuestions')

infile = read_file('data.json') #从data.json文件中读取题库

if infile:
    response = requests.get(url)

    questions = ''
    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.text,"html.parser") #使用pyhton内置库解析
        for content in soup.find_all('div',attrs={'class':'txtMg'}):
            question_content = content.find('span').get_text() #找到题目内容
            question_id = content.find('input',attrs={'type':'radio'}).get('class')[0][9:]  #找到题目编号

            question = "="*50 + "\n" + question_content + "\n\n" + infile[question_id]['answer'] + "\n"  # 一条问题和答案
            questions += question #添加到所有问题

    save_file(questions,'get_correct_answer.txt')  #匹配到的题目与答案保存到文件answer.txt

    print("生成答案成功! 答案已保存到：'get_correct_answer.txt'")
else:
    print("题库错误!")