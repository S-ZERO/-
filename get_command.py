 # -*- coding: Shift-JIS -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from time import sleep
import shutil, argparse, csv

import sys
import os

from bs4 import BeautifulSoup

from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from requests.exceptions import Timeout
from selenium.common.exceptions import TimeoutException

try:
    shutil.rmtree(r'Z:\���O���\�V�O�l�`���w���v')
except FileNotFoundError:
    pass
    
os.makedirs(r'Z:\���O���\�V�O�l�`���w���v')

result = []

#chorom.driver�݂̍菈���w��
driver = webdriver.Chrome(r'C:\Users\user\Desktop\���q�������O���\�菇���p�����R�}���h\chromedriver.exe') 

#URL�ɃA�N�Z�X����
driver.get('https://www.ibm.com/developerworks/community/wikis/home?lang=ja#!/wiki/W7aa8e6f6ff2b_45b7_b1a6_48254e608f0e/page/%E9%96%A2%E9%80%A3%E3%83%89%E3%82%AD%E3%83%A5%E3%83%A1%E3%83%B3%E3%83%88')

#�����R�}���h���\�������܂ő҂�
WebDriverWait(driver,60).until(
EC.presence_of_element_located((By.XPATH, '//*[@id="wikiContentDiv"]/div/p[16]'))
)

source = driver.page_source
soup = BeautifulSoup(source, "html.parser")

wikiCD = soup.select("div#wikiContentDiv")
a = wikiCD[0].select("a")

a_list = []
file_names = []
for download_file in a:
    a_list.append(download_file)
    file_name = download_file.text[-35:]
    file_names.append(file_name)

#-------------------------------�����R�}���h���쐬----------------------------------

#-----------------------------�������ʂ̃t�@�C���쐬-----------------------------
command = "copy /B"
for file in file_names:
    command = command + " " + file
    command = command + " + "
    
command = command.rstrip("+ ")


#�������ʂ̃t�@�C������yyyymmdd�������쐬
str_date = driver.find_element_by_xpath("/html/body/div[4]/div[2]/div[3]/div[2]/div[1]/div/p[2]")
str_date = str_date.text

date = datetime.strptime(str_date, '�ŏI�X�V�� : %Y�N%m��%d��')
year = str(date.year)

if date.month > 9: 
    month = str(date.month)
else:
    month = "0" + str(date.month)

if date.day > 9:
    day = str(date.day)
else:
    day = "0" + str(date.day)

#-----------------------------�������ʂ̃t�@�C�����쐬-----------------------------
result_filename = "xforcehelpfilesj" + year + month + day + ".tar.gz"

#-------------------------------�����R�}���h���쐬----------------------------------
command = command +" " + result_filename

driver.close()

#�擾���ʂ����
with open(r'Z:\���O���\�V�O�l�`���w���v\�����R�}���h.bat', mode='w') as f:
    #�R�}���h�����̂܂܃t�@�C���ɏ������ނƉ��s����Ȃ��āA���܂������Ȃ����炢�����񃊃X�g�ɓf���o��
    for download_file in a_list:
        sfn = download_file.text[-35:]
        f.write("bitsadmin /RawReturn /TRANSFER get " + download_file.text + " Z:\���O���\�V�O�l�`���w���v"+"\\" + sfn)
        f.write("\n")
 
    f.write(command)

print("����")
sys.exit(0)