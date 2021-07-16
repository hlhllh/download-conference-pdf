# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 14:38:25 2021

@author: Administrator
"""

"""
b'<div class="paper">\n'
b'  <p class="title">On the Convergence of Hamiltonian Monte Carlo with Stochastic Gradients</p>\n'
b'  <p class="details">\n'
b'    <span class="authors">Difan Zou,&nbsp;Quanquan Gu</span>;\n'
b'    <span class="info"><i>Proceedings of the 38th International Conference on Machine Learning</i>, PMLR 139:13012-13022</span>\n'
b'  </p>\n'
b'  <p class="links">\n'
b'    [<a href="http://proceedings.mlr.press/v139/zou21b.html">abs</a>][<a href="http://proceedings.mlr.press/v139/zou21b/zou21b.pdf" target="_blank" onclick="ga(\'send\', \'event\', \'PDF Downloads\', \'Download\', \'http://proceedings.mlr.press/v139/zou21b/zou21b.pdf\', 10);">Download PDF</a>][<a href="http://proceedings.mlr.press/v139/zou21b/zou21b-supp.pdf" target="_blank" onclick="ga(\'send\', \'event\', \'Extra Downloads\', \'Download\', \'Supplementary PDF\', 12);">Supplementary PDF</a>]</p>\n'
"""
import urllib
import os
import re

path = r'E:\Destback\test'
page = urllib.request.urlopen('http://proceedings.mlr.press/v139/')
rl_key_words = ['reinforce'] #, 'reinforcement', 'policy', 'markov', 'actor', 'q-value', 'critic', 'multi-agent']
rstr = r"[\/\\\:\*\?\"\<\>\|]"

def getFile(url, title = None):
    if title:
        file_name = '21-'+re.sub(rstr, "", title)
    else:
        file_name = url.split('/')[-1]
        
    try:
        u = urllib.request.urlopen(url)
    except urllib.error.HTTPError:
        #碰到了匹配但不存在的文件时，提示并返回
        # print(url, "url file not found")
        return
    block_sz = 8192
    full_path = os.path.join(path, file_name + '.pdf')
    with open(full_path, 'wb') as f:
        while True:
            buffer = u.read(block_sz)
            if buffer:
                f.write(buffer)
            else:
                break
    # print ("Sucessful to download" + " " + file_name)
            
def check(keywords, file_name):
    file_name = file_name.lower()
    if len(keywords) == 0:
        return True  # download all papers
    
    for key in keywords:
        if key in file_name:
            return True
    return False

papers = {}
title = None
for i in page.readlines():
    i = i.decode('UTF-8')
    if 'title' in i:
        title = i[19:-5]
    if '.pdf' in i:
        a = []
        b = None
        for b_index in range(len(i)):
            if i[b_index:b_index+4] =='http':
                a.append(b_index)
            if i[b_index-4:b_index] =='.pdf':
                b=b_index
                break
        link = i[a[-1]:b]
        if title:
            papers[title] = link
            
# doload according to papers
for paper in papers:
    if check(rl_key_words, paper):
        link = papers[paper]
        getFile(link, paper)