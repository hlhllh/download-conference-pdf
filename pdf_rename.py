# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 22:28:05 2020

@author: Administrator
"""

import os
from PyPDF2 import PdfFileWriter, PdfFileReader
from shutil import copy2
from io import StringIO
import re
 
pattern="[A-Z]"
rstr = r"[\/\\\:\*\?\"\<\>\|]"
src_dir = r'E:\onedrive-copy\OneDrive for Business 1\anaconda project\pdf_download'  # 源文件目录地址
des_dir = r'F:\onedrive\OneDrive - Nanyang Technological University\ICML20'  # 新文件目录地址
num = 0
 
def list_all_files(rootdir):
    import os
    _files = []
    l = os.listdir(rootdir) #列出文件夹下所有的目录与文件
    for i in range(0,len(l)): #len(l) 7
           path = os.path.join(rootdir,l[i])
           if os.path.isdir(path):
              _files.extend(list_all_files(path))
           if os.path.isfile(path):
              _files.append(path)
    return _files
 
if not os.path.exists(des_dir):  # 如果没有目标文件夹,新建一个目标文件夹进行存储
    os.makedirs(des_dir)
 
if os.path.exists(src_dir):
    files = list_all_files(src_dir)  # 获取源文件的目录地址
    for file in files:  # 对于目录下的每一个文件
        pdf_reader = PdfFileReader(open(file, 'rb'))  # 打开并建立一个PDF文件对象
        try:
            paper_title = pdf_reader.getDocumentInfo().title  # 获取PDF标题
        except:
            paper_title = None
        if paper_title == None:
            content = pdf_reader.getPage(0).extractText()
            buf = StringIO(content)
            paper_title = buf.readline()
            paper_title = re.sub(pattern,lambda x:" "+x.group(0),paper_title)[1:]
        print("num : %s" % num, paper_title)  # 显示处理到第几个文件
        num += 1
        paper_title = str(paper_title)  # 标题字符化
        paper_title = paper_title.replace('\n', '')
        if len(paper_title)>1000:
            paper_title = paper_title[:50]
        paper_title = re.sub(rstr, "", paper_title)
        if paper_title.find('/') != -1:  # 对于'/'无法写入文件名的情况,将其用'_'代替
            new_paper_title = paper_title.replace('/', '_')
            paper_title = '20-'+new_paper_title
            copy2(file, os.path.join(des_dir, paper_title) + '.pdf')
        else:
            copy2(file, os.path.join(des_dir, '20-'+paper_title) + '.pdf')
 
else:
    print("该路径下不存在所查找的目录!")