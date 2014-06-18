#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from math import sqrt
#You have to install the python lib
import jieba

def getsimilarity(str1, str2):
    str_words = {}
    ignore_list = [u'的',u'了',u'和',u'呢',u'啊',u'哦',u'恩',u'嗯',u'吧'];
    accepted_chars = re.compile(ur"[\u4E00-\u9FA5]+")
    
    all_the_text = str1
    seg_list = jieba.cut(all_the_text, cut_all=True)
    #print " ".join(seg_list)
    for s in seg_list:
        if accepted_chars.match(s) and s not in ignore_list:
            if s not in str_words.keys():
                str_words[s] = [1,0]
            else:
                str_words[s][0] += 1
            #end if
        #end if
    #end for
    
    all_the_text = str2
    seg_list = jieba.cut(all_the_text, cut_all=True)
    #print " ".join(seg_list)
    
    for s in seg_list:
        if accepted_chars.match(s) and s not in ignore_list:
            if s not in str_words.keys():
                str_words[s] = [0,1]
            else:
                str_words[s][1] += 1
            #end if
        #end if
    #end for

    sum_str = 0
    sum_str1 = 0
    sum_str2 = 0
    for word in str_words.values():
        sum_str += word[0]*word[1]
        sum_str1 += word[0]**2
        sum_str2 += word[1]**2
    #end for

    rate = sum_str/(sqrt(sum_str1*sum_str2))
    #rate = 0
    return rate

#end def

def file_reader(filename,filename2):
    file_words = {}
    ignore_list = [u'的',u'了',u'和',u'呢',u'啊',u'哦',u'恩',u'嗯',u'吧'];
    accepted_chars = re.compile(ur"[\u4E00-\u9FA5]+")

    file_object = open(filename)

    try:
        all_the_text = file_object.read()
        seg_list = jieba.cut(all_the_text, cut_all=True)
        #print "/ ".join(seg_list)
        for s in seg_list:
            if accepted_chars.match(s) and s not in ignore_list:
                if s not in file_words.keys():
                    file_words[s] = [1,0]
                else:
                    file_words[s][0] += 1
    finally:
        file_object.close()

    file_object2 = open(filename2)

    try:
        all_the_text = file_object2.read()
        seg_list = jieba.cut(all_the_text, cut_all=True)
        for s in seg_list:
            if accepted_chars.match(s) and s not in ignore_list:
                if s not in file_words.keys():
                    file_words[s] = [0,1]
                else:
                    file_words[s][1] += 1
    finally:
        file_object2.close()

    sum_2 = 0
    sum_file1 = 0
    sum_file2 = 0
    for word in file_words.values():
        sum_2 += word[0]*word[1]
        sum_file1 += word[0]**2
        sum_file2 += word[1]**2

    rate = sum_2/(sqrt(sum_file1*sum_file2))
    print 'rate: '
    print rate



#file_reader('thefile.txt','thefile2.txt')

