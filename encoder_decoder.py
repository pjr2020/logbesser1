from collections import Counter
import numpy as np

import tokenize as tk
from io import BytesIO

import just

import os

def text_tokenize(txt):
    """ 提取python文件中的token（并去掉空格） """
    """ 输入是字符串列表，每个字符串是一整个py文件 """
    """ 输出是一个列表的列表，外层列表每一项代表一个py文件的token列表，内列表每一项是一个token """
    toks = []
    try:
        for x in tk.tokenize(BytesIO(txt.encode('utf-8')).readline):
            toks.append(x)
    except tk.TokenError:
        pass
    tokkies = []
    old = (0, 0)
    for t in toks:
        if not t.string:
            continue
        if t.start[0] == old[0] and t.start[1] > old[1]:
            tokkies.append(" " * (t.start[1] - old[1]))
        tokkies.append(t.string)
        old = t.end
    if txt.endswith(" "):
        tokkies.append(" ")
    toks = [x for x in tokkies if not (x.startswith("#") or x.startswith('"""'))]
    return [x for x in toks[1:] if x != " "]

def replace(keyword):
    """ 预处理函数，将py文件中含有keyword的一行替代为keyword，便于处理 """
    dirs = os.listdir()
    for f in dirs:
        if os.path.splitext(f)[1] == ".py":
            print(os.path.splitext(f)[0])
            with open (f, 'r') as tempf:
                templist = tempf.readlines()
                for i, line in enumerate(templist):
                    if keyword in line:
                        templist[i] = keyword + '\n'
            with open(f, 'w') as tempf:
                for line in templist:
                    tempf.write(line)