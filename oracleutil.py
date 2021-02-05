#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/2/1 下午3:55
# @Author  : yaochong/Chongzi
# @FileName: oracleutil.py.py
# @Software: PyCharm
# @Blog    ：https://github.com/yaochong-06/ ; http://blog.itpub.net/29990276

import os
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import re

"""
搜索脚本
"""


def search():
    input_str = input("请输入要搜索内容：")
    lines = open('static/search.txt').readlines()
    for l in lines:
        tmp_str = l[0:50].replace('#', '')
        score = fuzz.ratio(tmp_str, input_str)
        if score > 30:
            res_list = ''.join(l).split('&&')
            for res in res_list:
                print(res.lstrip())
