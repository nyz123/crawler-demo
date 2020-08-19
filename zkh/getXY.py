# coding:utf-8
import urllib
import chardet
from urllib import request

url = 'http://www.ehsy.com/'
 
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
response = request.Request(url,headers) #
html = response.data
print(html)