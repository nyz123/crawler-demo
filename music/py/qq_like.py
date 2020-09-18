import requests
import csv
from bs4 import BeautifulSoup
import urllib.request
from pathlib import Path
import os
import time

url = 'https://y.qq.com/n/yqq/playlist/2459598034.html'
file_path = 'F:\\xdl\\github\\crawler-demo\\music\\data\\'
headers={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    # 'cookie': 'pgv_pvid=😊; tvfe_boss_uuid=5e066b86b31da004; pgv_pvi=1049682944; RK=sgjkSZiyWa; ptcz=f988bba111b1b9da696c407070a15767dc81e10d7d5d791982ae983433da9f37; yfx_step_rand_default_10004089=1588216637503; yfx_c_g_u_id_10004089=_ck20200430111717621533244023105; yfx_f_l_v_t_10004089=f_t_1588216637503__r_t_1588216637503__v_t_1588216637503__r_c_0; _ga=GA1.2.733654307.1588216638; XWINDEXGREY=0; eas_sid=3NZNJLLHL8MNqr0GXrhaKqs8Rq; LW_sid=a105M9M3x5e0l4g0e4K4e4o0H2; LW_uid=21w5h9z34520M4m034k4e4r0V4; o_cookie=1083206106; pac_uid=1_1083206106; ptui_loginuin=1083206106; pgv_si=s4358755328; _qpsvr_localtk=0.06238628146556935; pgv_info=ssid=s4566938693; ts_refer=www.baidu.com/link; ts_uid=1022116778; psrf_qqopenid=72A94270FAC4FF5CF291980175C49D98; psrf_qqrefresh_token=C0D023821BF823E279BBE14A7AE747B8; psrf_qqunionid=; qqmusic_key=Q_H_L_2WSkXz50eWu9Tsh7Vpv5LrvD-1Xpz6nnRYHuyAF1etN7ae6f5xUpTevVUbDL778; euin=oKnFoi-z7w6z7c**; psrf_qqaccess_token=DA9D46D05494864BE6BE8367DAF62068; tmeLoginType=2; psrf_musickey_createtime=1600240072; uin=1083206106; psrf_access_token_expiresAt=1608016072; qm_keyst=Q_H_L_2WSkXz50eWu9Tsh7Vpv5LrvD-1Xpz6nnRYHuyAF1etN7ae6f5xUpTevVUbDL778; userAction=1; yqq_stat=0; ts_last=y.qq.com/n/yqq/playlist/2459598034.html'
}

def get_data(url):
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text,'html.parser',from_encoding='utf-8')
    print(soup.find_all(class_='songlist__songname_txt'))

if __name__ == '__main__':
    get_data(url)
