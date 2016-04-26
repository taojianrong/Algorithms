# -*- coding:utf-8 -*- #
#! /usr/bin/env python

import urllib
import urllib2
import string
import sys
import re
import random
import socket
from bs4 import BeautifulSoup
from time import time
from threading import Thread
from Queue import Queue
from time import sleep

def search(keyword, year, retries=32):
    url = "http://epub.sipo.gov.cn/gjcx.jsp/patentoutline.action"
    values = {
        'numFMGB' : '0',
        'numFMSQ' : '0',
        'numSYXX' : '0',
        'numSortMethod' : '4',
        'numWGSQ' : '0',
        'pageNow' : '1',
        'pageSize' : '3',
        'selected' : '',
        'showType' : '1',
        'strLicenseCode' : '',
        'strWord' : "申请日=BETWEEN['" + str(year) + ".01.01','" + str(year) + ".12.31'] and 申请（专利权）人='" + keyword + "'",
    }
    data = urllib.urlencode(values)
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
        'Referer':'http://epub.sipo.gov.cn/gjcx.jsp'
    }
    try:
        req = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(req)
        the_page = response.read()
        pool = BeautifulSoup(the_page)
    except:
        if retries > 0:
            sleep(1)
            return search(keyword, year, retries-1)
        else:
            print 'GET Failed!!!'
            return [[-1,-1,-1,-1], keyword]

    try:
        tmp  = pool.find('dl',attrs = {'class':"lxxz_dl"})
        tmp1 = tmp.findAll('li')
    except:
        print 'GET Nothing!!!'
        return [[0,0,0,0], keyword]

    eachNum = []  # 四类专利各自数量
    for node in tmp1:
        pattern = re.compile('(\d+)')
        num = re.search(pattern, node.string)
        eachNum.append(string.atoi(num.group(1)))
    res = [eachNum, keyword]  #  返回两项内容：res[0]是各类专利数量  res[1]是年份统计字典
    print 'GET Successed!!!'
    return res


##### main函数
def main():
    q = Queue()     # q是任务队列
    JOBS = len(c)   # JOBS是有多少任务

    def spiderNet(arguments):    #具体的处理函数，负责处理单个任务
            global count
            company = []
            company.append(c[arguments])
            SSX(c[arguments], company)
            del(company[0])
            company = list(set(company))
            company.append(c[arguments])
            # for i in range(len(company)):
            #     print(company[i].decode('utf-8').encode('utf-8'))

            data = search(company[len(company)-1], year)
            argumentList[arguments] = arguments
            companyList[arguments] = data[1]
            dataList[arguments] = data[0]
            flagList[arguments] = 0

            flag = 1
            if data[0] == [0,0,0,0]:
                flag = 0

            for i in range(len(company)-1):
                data = search(company[i], year)
                argumentList1[arguments*10+i] = arguments
                companyList1[arguments*10+i] = data[1]
                dataList1[arguments*10+i] = data[0]
                if (data[0] != [0,0,0,0])&(flag == 0):
                    flagList[arguments] = 1
                if (data[0] != [0,0,0,0])&(flag == 1):
                    flagList[arguments] = 2
                if (data[0] == [0,0,0,0])&(flag == 1):
                    flagList[arguments] = 3

            count += 1
            print(str(count) + " finished!!!")

            if (count == n) | (count%100 == 0):
                #将爬取的数据写入CSV1文件内
                out = open(str(year)+".csv1", "w")
                for i in range(len(dataList1)):
                    if (type(dataList1[i]) == type(1)):
                        pass
                    else:
                        line = str(argumentList1[i]) + ","
                        line += companyList1[i]
                        for w in dataList1[i]:
                            line += ","
                            line += str(w)
                        line += "\n"
                        out.write(line)
                out.close()

                #将爬取的数据写入CSV文件内
                out = open(str(year)+".csv", "w")
                for i in range(len(dataList)):
                    if (type(dataList[i]) == type(1)):
                        pass
                    else:
                        line = str(flagList[i]) + ","
                        line = line + str(argumentList1[i]) + ","
                        line += companyList[i]
                        for w in dataList[i]:
                            line += ","
                            line += str(w)
                        line += "\n"
                        out.write(line)
                out.close()

                print "END Spider!!!\n"


    def working():  #这个是工作进程，负责不断从队列取数据并处理
            while True:
                    arguments = q.get()
                    print(str(arguments) + " in thread!!!\n")
                    spiderNet(arguments)
                    q.task_done()

    for job in range(JOBS): #把JOBS排入队列
            q.put(job)

    for i in range(NUM):    #fork NUM个线程等待队列
            t = Thread(target = working)
            t.setDaemon(True)
            t.start()

    q.join()



##### 爬虫初始化 ############################
def spiderInit():
    ### 使用代理服务器,
    proxy_support = urllib2.ProxyHandler({'http':'http://'+random.choice(IPlist)})
    opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)

def fileInit():
    f = open("ip.csv", "r")
    while True:
        line = f.readline()
        if line:
            pass
            line = line.replace("\"","")
            line = line.replace("\n","")
            line = line.replace(",","")
            IPlist.append(line)
        else:
            break
    f.close()
    print("－－－读取IP列表成功－－－")
    ########################################
    f = open("input.csv", "r")
    while True:
        line = f.readline()
        if line:
            pass
            line = line.replace("\'","")
            line = line.replace("\n","")
            line = line.replace(",","")
            c.append(line)
        else:
            break
    f.close()
    print("－－－导入公司数据完成－－－")
    ########################################
    f = open("area.csv", "r")
    while True:
        line = f.readline()
        if line:
            pass
            line = line.split(',')
            area.append({'ssx1':line[1], 'ssx2':line[2], 'isused1':0, 'isused2':0})
        else:
            break
    f.close()
    print("－－－导入省市县数据完成－－－")
    ########################################

def SSX(keyword, company):
    tag1 = []
    tag2 = []
    for i in range(N):
        chazhao1 = keyword.find(area[i]['ssx1'])
        if (chazhao1 != -1):
            tag1.append(i)
        else:
            chazhao2 = keyword.find(area[i]['ssx2'])
            if (chazhao2 != -1):
                tag2.append(i)
    for i in range(len(tag1)):
        for j in range(len(company)):
            company.append(company[j].replace(area[tag1[i]]['ssx1'], area[tag1[i]]['ssx2']))
    for i in range(len(tag2)):
        for j in range(len(company)):
            company.append(company[j].replace(area[tag2[i]]['ssx2'], area[tag2[i]]['ssx1']))


##### 程序主入口 ############################
if __name__ == '__main__':

    ### 设置timeout延迟 #####################
    socket.setdefaulttimeout(10)
    ########################################
    IPlist = []          ### IP集合
    c = []               ### 申请人集合
    area = []            ### 省市县集合
    fileInit()           ### 初始化上述三项
    ########################################
    n = len(c)
    N = len(area)
    year = 1992  ### 设置专利申请年份
    NUM = 16    ### 并发线程总数
    count = 0
    argumentList = range(n)
    companyList = range(n)  ### 存储公司标示
    dataList = range(n)     ### 存储专利数据
    flagList = range(n)     ### 存储是否修改省市县
    argumentList1 = range(10*n)
    companyList1 = range(10*n)  ### 存储公司标示
    dataList1 = range(10*n)     ### 存储专利数据
    ########################################
    main()
    ########################################



