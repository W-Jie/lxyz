# encoding: utf-8

import requests
import bs4 
import time
import json
import re

# pip install requests beautifulsoup4


# 保存json文件
def save_file_with_json(_data,_file):
    with open(_file, 'w', encoding='utf-8') as outfile:
        json.dump(_data, outfile, ensure_ascii=False)

# 保存文件
def save_file(_data,_file):
    with open(_file, 'w', encoding='utf-8') as outfile:
        outfile.write(_data)

# 当前时间
def current_time():
    return time.strftime('%Y-%m-%d %X',time.localtime())

# 当前时间（时间戳）
def now():
    return time.time()


def collect():
    result = {} # 爬虫收集结果
    all_questions = '' # 所有题目和答案
    answerHisStartNum = 1  #历史试题，用于收集题库。开始采集试题编号
    answerCnt = 50  #收集历史试卷数量。如果发现答案有错，需要调整开始值及数量值

    for num in range(answerHisStartNum, answerHisStartNum + answerCnt):
        url = 'http://ks.gdycjy.gov.cn/kQuestion.shtml?act=getHistory&pageSize=50&kAnswerInfoId=' + str(num) #pageSize=50 一次显示50道题目

        response = requests.get(url)
        if response.status_code == 200: #判断url是否可访问。url通过iframe嵌套，貌似都是返回200
            # print(response.status_code)
            soup = bs4.BeautifulSoup(response.text,"html.parser")

            for content in soup.find_all('div',attrs={'class':'txtMg'}):  # 题目与答案分块
                question_content = content.find('span').get_text() #找到题目内容

                if (question_content.find('此题回答错误') <0):  # 题目中如有提示回答错误，则跳过采集
                    answer = content.find('input',attrs={'type':'radio'},checked=True) #找到已选中的正确答案
                    answer_content = answer.parent.get_text() # 找到已选答案的内容
                    question_id = answer.get('class')  #通过答案的class找到题目编号

                    # 题目中有显示“正确答案是”的话，即已选中答案为错误。因此只记录正确的答案与题目
                    # 使用错误捕获的方式，如果题目没有显示“正确答案是”，find出来的type为NoneType，无法再进行get操作，捕获错误进而保存回答正确的题目
                    # result结构：{'题目id' = {'question':'题目id+题目','answer':'正确答案'}}
                    try:
                        correct_answer = content.find('input',class_="xhx").get('value')
                    except Exception as e:
                        result[question_id[0][9:]] = {"question":question_id[0][9:]+"、"+question_content.split('、',1)[1],"answer":answer_content.strip("\n")}
        else:
            print("worng URL:",url)

    # 格式化题目和答案,并持久化保存
    if result:
        for id in result:
            all_questions += "="*50 + "\n" + result[id]['question'] + "\n\n" + result[id]['answer'] + "\n"
        save_file_with_json(result,'data.json')
        save_file(all_questions,'questions.txt')
        print("题库采集成功，题库数量共 %d，题库已保存到文件'questions.txt'" % len(result))
    else:
        print("Error: 题库采集失败!")

if __name__ == '__main__':
    print(current_time())
    start_time = now()
    collect()
    print("time: %.2f" %(now()-start_time))
