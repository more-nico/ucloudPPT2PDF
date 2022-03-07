from sysconfig import get_python_version
import requests 
from bs4 import BeautifulSoup
import requests,sys,webbrowser,bs4,re
import os
import sys
import time
import numpy as np
import glob
import fitz
os.environ['REQUESTS_CA_BUNDLE'] =  os.path.join(os.path.dirname(sys.argv[0]), 'cacert.pem')

def mkdir(path):
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
 
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
 
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path) 
 
        print (path+' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print (path+' 目录已存在')
        return False

# 获取网站返回的状态码
def getHttpStatusCode(url):
    try:
        request = requests.get(url)
        httpStatusCode = request.status_code
        return httpStatusCode
    except requests.exceptions.HTTPError as e:
        return e

def pic2pdf_1(img_path, pdf_path, pdf_name):
    doc = fitz.open()

    for img in sorted(glob.glob(img_path + "\*.jpg")):
        imgdoc = fitz.open(img)
        pdfbytes = imgdoc.convert_to_pdf()
        imgpdf = fitz.open("pdf", pdfbytes)
        doc.insert_pdf(imgpdf)
    doc.save(pdf_path + pdf_name)
    doc.close()

def del_file(path_data):
    for i in os.listdir(path_data) :# os.listdir(path_data)#返回一个列表，里面是当前目录下面的所有东西的相对路径
        file_data = path_data + "\\" + i#当前文件夹的下面的所有东西的绝对路径
        if os.path.isfile(file_data) == True:#os.path.isfile判断是否为文件,如果是文件,就删除.如果是文件夹.递归给del_file.
            os.remove(file_data)
        else:
            del_file(file_data)


url = input("请输入PPT页面第一页的图片链接：")
mkdir("cache")
pdf_path = os.getcwd()
img_path = pdf_path+'\\cache'
jpg_str = "cache/1.jpg"
jpg_list = []
str_list = []

for j in jpg_str:
    jpg_list.append(j)
for j in url:
    str_list.append(j)

url1 = url
str_list1 = []
for j in url1:
    str_list1.append(j)
tmp_H = 512
tmp_L = 1
tmp = 1
for i in range(1000):
    print("\r", end="")
    print("解析中...",end="")
    url_status = getHttpStatusCode(url1)
    if((tmp_H-tmp_L)>5):
        if((url_status==404)|(url_status==414)):
            tmp_H = tmp
            tmp = int((tmp_H+tmp_L)/2)
        else:
            tmp_L = tmp
            tmp = int((tmp_H+tmp_L)/2)
    else:
        if(url_status==404):
            print("解析完成，共有"+str(tmp)+"页")
            break
        tmp = tmp_L
        tmp_L+=1
    str_list1[-5] = str(int(tmp)+1)
    url1 = "".join(str_list1)

scale = tmp
print("开始下载".center(scale // 2,"-"))
start = time.perf_counter()
for i in range(1000):
    if os.path.exists(img_path+'\\'+str(i+1)+'.jpg'):
        tmp = str_list[-5]
        str_list[-5] = str(int(tmp)+1)
        url = "".join(str_list)
        print("第"+str(i+1)+"页已下载，跳过")
        continue
    url_status = getHttpStatusCode(url)
    if(url_status==404):
        print("下载完成")
        break
    r = requests.get(url)
    with open(jpg_str, "wb") as code:
        code.write(r.content)
    tmp = str_list[-5]
    str_list[-5] = str(int(tmp)+1)
    url = "".join(str_list)
    tmp = jpg_list[-5]
    jpg_list[-5] = str(int(tmp)+1)
    jpg_str = "".join(jpg_list)
    a = "*" * i
    b = "." * (scale - i)
    c = (i / scale) * 100
    dur = time.perf_counter() - start
    print("\r{:^3.0f}%[{}->{}]{:.2f}s".format(c,a,b,dur),end = "")
    time.sleep(0.1)

pic2pdf_1(img_path=img_path, pdf_path=pdf_path, pdf_name=r'\output.pdf')
print("PDF生成完毕")
os.startfile(pdf_path+'\\output.pdf')

del_file(img_path)

