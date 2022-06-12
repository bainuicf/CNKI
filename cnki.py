'''
@文件    :cnki.py
@说明    :利用selenium爬取cnki搜索结果
@时间    :2022/04/18 02:09:35
@作者    :ShellC
@版本    :1.0
'''
#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
from time import sleep
from selenium import webdriver

def cnki_search(keyword):
    # 输入CNKI网址
    url= 'https://www.cnki.net/'
    # url= 'https://kns.cnki.net/kns8/defaultresult/index'
    bro= webdriver.Edge(executable_path='msedgedriver.exe')
    bro.get(url)
    # 输入关键词
    search_box= bro.find_element_by_class_name('search-input')
    search_btn= bro.find_element_by_class_name('search-btn')
    search_box.send_keys(keyword)
    search_btn.click()
    sleep(2)
    # 切换外文库
    switch= bro.find_element_by_class_name('en')
    switch.click()
    sleep(2)
    # 存放结果
    result=[]
    # 判断结果是否为空
    if isElementExist(bro,'PageNext')==False:
        print('无搜索结果')
        return result

    # 获取下一页标签
    next_page= bro.find_element_by_id('PageNext')    
    # 获取搜索结果总数
    result_num= bro.find_element_by_class_name('pagerTitleCell')
    print(result_num.text)

    # 如果有下一页标签则继续
    while isElementExist(bro,'PageNext'):
        # 获取搜索结果：序号、题目、作者、来源、发表时间、数据库
        num_list= bro.find_elements_by_class_name('seq')
        name_list= bro.find_elements_by_class_name('name')
        author_list= bro.find_elements_by_class_name('author')
        source_list= bro.find_elements_by_class_name('source')
        time_list= bro.find_elements_by_class_name('date')
        data_list= bro.find_elements_by_class_name('data')
        # 结果写入字典
        for i in range(len(name_list)):
            result.append({
                '序号': num_list[i].text,
                '题目': name_list[i].text,
                '作者': author_list[i].text,
                '来源': source_list[i].text,
                '日期': time_list[i].text,
                '文献库': data_list[i].text
            })
        # 点击下一页
        next_page= bro.find_element_by_id('PageNext')
        next_page.click()
        sleep(2)
    return result


def isElementExist(bro, element):
    try:
        bro.find_element_by_id(element)
        return True
    except Exception as e:
        return False

if __name__ == '__main__':
    # 输入搜索关键词
    keyword= input('请输入搜索关键词：')
    result= cnki_search(keyword)
    if len(result)==0:
        print("结果为空")
        os._exit()
    # 判断result文件是否存在
    filename= 'result.xls'
    if os.path.exists(filename):
        os.remove(filename)
    # 写入json文件
    # with open(filename,'a', encoding='utf-8') as fp:
    #     json.dump(result, fp, ensure_ascii= False)
    # # 写入excel文件
    import pandas as pd
    df= pd.DataFrame(result)
    df.to_excel('result.xls',index= False)
