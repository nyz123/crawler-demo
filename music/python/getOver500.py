# -*- coding:utf-8 -*- 
import urllib2
import requests
from pprint import pprint
from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import sys   #reload()之前必须要引入模块
reload(sys)
sys.setdefaultencoding('utf-8')

#向指定的url地址发送请求，并返回服务器响应的类文件对象
#服务器返回的类文件对象支持python文件对象的操作方法
#read()方法就是读取文件里的全部内容，返回字符串
# 用PhantomJS创建一个Selenium的WebDriver
url = 'https://music.163.com/#/discover/playlist'
driver = webdriver.PhantomJS()

csv_file = open('../data/playlist.csv','w')
writer = csv.writer(csv_file)
writer.writerow(['标题','播放数','链接',])
# 解析每一页，直到下一页为空
page = 1
while url != 'javascript:void(0)':
    # 用webdriver加载页面
    driver.get(url)
    # 切换到内容的iframe
    driver.switch_to.frame('contentFrame')
    # 定位歌单标签
    data = driver.find_elements_by_css_selector('.p-pl .m-cvrlst li')
    print 'page:',page,'.',len(data)
    # 解析一页中的歌单
    for i in range(len(data)):
        # 获取播放数
        nb = data[i].find_element_by_class_name('nb').text
        if '万' in nb and int(nb.split('万')[0])>500:
            # 获取播放量大于500万的歌单封面
            msk = data[i].find_element_by_css_selector('a.msk')
            # 把封面标题/链接/播放数放入文件
            writer.writerow([msk.get_attribute('title'),nb,msk.get_attribute('href')])
            print 'YES:',msk.get_attribute('title').encode("gbk", 'ignore').decode("gbk", "ignore"),nb

    # 定位下一页的url
    url = driver.find_element_by_css_selector('a.zbtn.znxt').get_attribute('href')
    page = page + 1
csv_file.close()
