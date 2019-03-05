# -*- coding:utf-8 -*- 
from selenium import webdriver
import csv
import sys   #reload()之前必须要引入模块
reload(sys)
sys.setdefaultencoding('utf-8')

#向指定的url地址发送请求，并返回服务器响应的类文件对象
#服务器返回的类文件对象支持python文件对象的操作方法
#read()方法就是读取文件里的全部内容，返回字符串
# 用PhantomJS创建一个Selenium的WebDriver
# url = 'https://music.163.com/#/my/m/music/playlist?id=938817542'
url = 'https://music.163.com/#/my/m/music/playlist?id=997386069'
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options)
# driver = webdriver.PhantomJS()

csv_file = open('../data/music.csv','w')
writer = csv.writer(csv_file)
writer.writerow(['歌名','id','src'])
# 解析每一页，直到下一页为空
# 用webdriver加载页面
driver.get(url)
# 切换到内容的iframe
driver.switch_to.frame('contentFrame')
# 定位歌单标签
data = driver.find_elements_by_css_selector('.m-table tr .txt a')
# 解析一页中的歌单
for i in range(len(data)):
    name = data[i].find_element_by_tag_name('b').get_attribute('title') 
    link = data[i].get_attribute('href')
    writer.writerow([name.encode('utf-8'),link])
    songUrl = link
    print('music:',i+1,', successful')
csv_file.close()

