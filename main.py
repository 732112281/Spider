import re
from Chinese_to_Arabic import chinese_to_arabic
string = "第三章 hehe"
titles = re.findall("第(.*?)章(.*?)>", string+'>')
print(titles)
for title in titles:
    title1, title2 = title
    try:
        title1 = int(title1)
    except:
        title1 = chinese_to_arabic(title1)
print('第'+str(title1)+'章'+title2)