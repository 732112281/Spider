# coding:utf-8
import requests
import threading
from bs4 import BeautifulSoup
import re
import os
from Chinese_to_Arabic import chinese_to_arabic

req_url_base='http://www.qu.la/book/'           #小说主地址
threadLock = threading.Lock()
treads = []
# 小说下载函数
# txt_id：小说编号
# txt字典项介绍
# id：小说编号
# title：小说题目
# first_page：第一章页面
# txt_section：章节地址
# section_name：章节名称
# section_text：章节正文
# section_ct：章节页数

def get_txt(txt_id):
    txt = {}
    txt['title'] = ''
    txt['id'] = str(txt_id)
    have_written, have_existed, write_failed = 0, 0, 0
    try:
        # print("请输入需要下载的小说编号：")
        # txt['id']=input()
        req_url = req_url_base + txt['id']+'/'  # 根据小说编号获取小说URL
        print("小说编号："+txt['id'])
        res = requests.get(req_url)             # 获取小说目录界面
        soups = BeautifulSoup(res.text, "lxml")         # soup转化
        # 获取小说题目
        txt['title'] = soups.select('#wrapper .box_con #maininfo #info h1')[0].text
        print("小说名：《"+txt['title']+"》  开始下载。")
        # 新建一个文件夹,保存小说内容
        path = "D:/小说/" + txt['title']
        if not os.path.exists(path):
            os.mkdir(path)
        # 转换路径
        os.chdir(path)
        print("存储地址:" + path)
        print("正在获取所有章节地址。。。")
        # 获取小说所有章节信息
        all_page_address = soups.select('#wrapper .box_con #list dl dd a')
        # 获取小说总章页面数
        section_ct = len(all_page_address)
        print("小说章节页数："+str(section_ct))
        # 获取每一章节信息
        for one_page_info in all_page_address:
            try:
                # 筛选信息
                if 'book' not in one_page_info["href"]:
                    continue
                # 请求当前章节页面
                r = requests.get(req_url+str(one_page_info['href']))
                # soup转换
                soup = BeautifulSoup(r.text, "lxml")
                # 获取章节名称
                section_name = soup.select('#wrapper .content_read .box_con .bookname h1')[0]
                # 清洗章节名称
                t = (section_name.text + '>').replace('草', '章')
                # 拆分章节名称
                section_names = re.findall("第(.*?)章(.*?)>", t)[0]
                # 把数据从元组类型转换为列表类型，便于更改
                section_names = list(section_names)
                # 把中文数字改为阿拉伯数字
                try:
                    int(section_names[0])
                except:
                    section_names[0] = chinese_to_arabic(section_names[0])
                # 清洗标题
                section_names[1] = re.sub(r"[^\w\s]", "", section_names[1])
                # 补全完整章节名称
                section_name = ('第%s章 ' % str(section_names[0])) + section_names[1]
                # 避免重复写入
                if os.path.exists('%s.txt' % section_name):
                    print(txt['title']+' 章节《' + section_name + '》已存在，取消写入')
                    have_existed += 1
                    continue
                # 设置标题格式
                title = section_name + '\n\n\n'
                # 获取章节文本
                section_text = soup.select('#wrapper .content_read .box_con #content')[0]
                # 清洗章节文本
                for ss in section_text.select("script"):   # 删除无用项
                    ss.decompose()
                section_text = re.sub('\s+', '\r\n\t', section_text.text).strip('\r\n')
                section_text = section_text.replace('\n', '\n\n')
                # 每隔一定字符，换行
                section_text = '\n'.join(re.findall('.{1,42}', section_text))
                with open("%s.txt" % section_name, "w", encoding="utf-8") as fo:
                    # 以二进制写入章节题目
                    # 把\t换为7个空格
                    title = title.expandtabs(7)
                    fo.write(title)
                    # 以二进制写入章节内容
                    # 把\t换为7个空格
                    section_text = section_text.expandtabs(7)
                    fo.write(section_text)
                    print(txt['title']+' 章节：' + section_name + '     已下载')
                    have_written += 1
                    # print(section_text.text.encode('UTF-8'))
            except:
                print("小说名：《"+txt['title']+"》 章节下载失败，正在重新下载。")
                write_failed += 1
    except:
        print("小说编号:%s，下载失败" % txt_id)
    else:
        print("小说编号:%s，名称：《%s》 下载完毕" % (txt_id, txt['title']))
        print('\n写入失败文件数\n写入文件数\n已存在文件数' %
              (str(write_failed), str(have_written), str(have_existed)))


# 此处为需要下载小说的编号，编号获取方法在上文中已经讲过。
get_txt(46516)