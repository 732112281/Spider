#coding:utf-8
import requests, re, os
from Chinese_to_Arabic import chinese_to_arabic
#下载一个网页
url = 'https://www.qu.la/book/46516/'

#模拟浏览器发送https请求
while True:
    try:
        response = requests.get(url)
        break
    except:
        continue

#编码方式
response.encoding = 'utf-8'

#目标小说主页的网页源码
html = response.text

#小说的名称
title = re.findall(r'<meta property="og:title" content="(.*?)" />', html)[0]

#新建一个文件夹,保存小说内容
path = "D:/小说/"+title
print(path)
if not os.path.exists(path):
    os.mkdir(path)
    
#获取每一章的信息(url,章节)
dl = re.findall(r'<dt>《科技图书馆》正文卷</dt>(.*?)</dl>', html, re.S)[0]
chapter_info_list = re.findall(r'<a style="" href="(.*?)">第(.*?)章(.*?)</a></dd>', dl)
#设置成功写入的文件和已存在的文件个数初始值
have_written, have_downloaded, write_failed = 0, 0, 0

#循环每一个章节,分别去下载
for chapter_info in chapter_info_list:
    try:
        # chapter_url = chapter_info[0]
        # chapter_title1 = chapter_info[1]
        # chapter_title1 = chapter_info[2]
        chapter_url, chapter_title1, chapter_title2 = chapter_info
        try:
            chapter_title1 = int(chapter_title1)
        except:
            chapter_title1 = chinese_to_arabic(chapter_title1)
        chapter_title = '第' + str(chapter_title1) + '章 ' + chapter_title2
        chapter_title = re.sub(r"[^\w\s]", "", chapter_title)

        # 转换路径
        os.chdir(path)

        # 避免重复写入

        if os.path.exists('%s.txt' % chapter_title):
            print(chapter_title + '\t\t文件已存在')
            have_downloaded += 1
            continue

        # 补全章节的url
        chapter_url = "https://www.qu.la%s" % chapter_url

        # 下载章节内容
        chapter_response = requests.get(chapter_url)
        chapter_response.encoding = 'utf-8'
        chapter_html = chapter_response.text
        chapter_contents = re.findall(r'<div id="content">(.*?)</br>', chapter_html, re.S)
        try:
            # 写入文件
            with open('%s.txt' % chapter_title, 'w', encoding='utf-8') as f:
                # 清洗数据
                for chapter_content in chapter_contents:
                    chapter_content = chapter_content.replace('&lt;!--divstyle="color:#f00"', '')
                    chapter_content = chapter_content.replace('Ｘ２３ＵＳ．ＣＯＭ', '')
                    chapter_content = chapter_content.replace('& nbsp;', '')
                    chapter_content = chapter_content.replace('　　', '')
                    chapter_content = chapter_content.replace('&nbsp;<br />', '')
                    chapter_content = chapter_content.replace('<br />', '\n\t')
                    chapter_content = chapter_content.replace('&nbsp;&nbsp;&nbsp;&nbsp;', '\n\t')
                    chapter_content = chapter_content.replace('&nbsp;', '\n\t')
                    chapter_content = chapter_content.replace('<br/>', '')
                    chapter_content = chapter_content.replace('\n\t\n\t\n\t', '')
                    chapter_content = chapter_content.replace('\n\t\n\t', '')

                    # 持久化
                    chapter_content = '\n'.join(re.findall('.{1,42}', chapter_content))
                    chapter_content = chapter_content.replace('\t', '\n\t')
                    chapter_content = chapter_content.expandtabs(7)
                    if not chapter_content.startswith(' '):
                        chapter_content = '       ' + chapter_content
                    f.write(chapter_title + '\n\n' + chapter_content)
        except:
            print(chapter_title + '\t\t写入失败')
            write_failed += 1
            continue

        else:
            print(chapter_title + '\t\t写入文件')
            have_written += 1
    except:
        continue

print('\n写入完成\n写入失败文件数' + str(write_failed) + '\n写入文件数' + str(have_written) +
      '\n已存在文件数' + str(have_downloaded))
exit()