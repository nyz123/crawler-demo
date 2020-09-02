import requests
import csv
from bs4 import BeautifulSoup
import urllib.request
from pathlib import Path
import os
import time
import json

url = 'https://job.bytedance.com/api/v1/search/job/posts?keyword=%E5%89%8D%E7%AB%AF&limit=10&offset=0&job_category_id_list=&location_code_list=CT_125&subject_id_list=&recruitment_id_list=&portal_type=2&portal_entrance=1&_signature=bY-qKwAAAACBs9EZXDSv.22PqjAADLO'

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}

response = requests.post(url,{"keyword":"前端","limit":10,"offset":0,"job_category_id_list":[],"location_code_list":["CT_125"],"subject_id_list":[],"recruitment_id_list":[],"portal_type":2,"portal_entrance":1},headers=headers)
# res_json = json.loads(response.text)

print(response)