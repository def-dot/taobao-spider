# *-* coding:utf-8 *-*
import requests
from bs4 import BeautifulSoup
import re
import pymysql


def get_page(url):
    content = requests.get(url)
    return content.content


if __name__ == '__main__':
    taobao2 = "https://2.taobao.com/list/"
    html = get_page(taobao2)
    soup = BeautifulSoup(html)
    links = soup.find_all(attrs={"href": re.compile('^//s[.]2[.]taobao[.]com/list/list[.]htm')}, limit=59)

    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "root", "taobao2")

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    for link in links:
        # # url编号
        # print(link.get('href')[45: 53])
        # # 分类
        # print(link.text)

        category = link.text
        code = link.get('href')[45: 53]

        # SQL 插入语句
        # sql = "INSERT INTO t_category (category, code) VALUES (%s, %s)"
        # parm = (category, code)
        sql = "INSERT INTO t_category (category, code) VALUES ('{}', '{}')" .format(category, code)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            print('插入成功')
        except:
            # 如果发生错误则回滚
            db.rollback()
            print('插入失败')

    # 关闭数据库连接
    db.close()





