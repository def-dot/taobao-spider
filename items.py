import time

from bs4 import BeautifulSoup
import requests
import pymysql


def make_url(catid, page):
    part1 = "https://s.2.taobao.com/list/?search_type=item&_input_charset=utf8&"
    part2 = "catid=" + str(catid)
    part3 = "&page=" + str(page)
    return part1 + part2 + part3


def get_catid(id):
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "root", "GraduationProject")

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    sql = "SELECT code FROM tb_taobao2_category WHERE id = {} LIMIT 1".format(id)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        result = cursor.fetchone()
        return "".join(result)
    except:
        print("Error: unable to fetch data")

    # 关闭数据库连接
    db.close()
    return


def get_items_by_category(cateid, number):
    for x in range(1, number+1):
        print("第", x, "页开始-------++++++++++++++++++++++++++++++++++++----------  ")
        time.sleep(3)
        url = make_url(get_catid(cateid), x)
        html = requests.get(url).content
        soup = BeautifulSoup(html, features="html.parser")
        divs = soup.find_all(attrs={"class": "ks-waterfall", "data-spm": "2007.1000337.16"}, limit=16)

        # 打开数据库连接
        db = pymysql.connect("localhost", "root", "root", "GraduationProject")

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        for div in divs:
            username = div.find(attrs={"class": "seller-nick"}).text[:-1]
            userpage_url = div.a['href'][2:]
            user_avatar = "wwc.alicdn.com/avatar/getAvatar.do?userNick="+username+"&type=sns"
            try:
                user_level = div.find_all('span')[1]['title']
            except:
                user_level = "none"
            item_info = div.find_all('a')[2]
            item_url = item_info['href'][2:]
            item_title = item_info['title']
            item_image = item_info.find('img')['data-ks-lazyload-custom'][2:]
            item_info2 = div.find(attrs={"class": "item-attributes"})
            item_price = item_info2.find('em').text
            item_location = item_info2.find(attrs={"class": "item-location"}).text
            item_desc = div.find(attrs={"class": "item-brief-desc"}).text
            t = time.time()
            ctime = int(t)
            mtime = ctime
            pics = BeautifulSoup(requests.get("https://"+item_url).content, features="html.parser").find_all(
                attrs={"class": "big-img"})

            # 插入 item 数据库
            sql = "INSERT INTO tb_taobao2_items_info (username, userpage_url, user_avatar, user_level, item_url," \
                  "item_title, item_image, item_price, item_location, item_desc, ctime, mtime) " \
                  "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"\
                .format(username, userpage_url, user_avatar, user_level, item_url, item_title, item_image, item_price,
                        item_location, item_desc, ctime, mtime)
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
                print('插入成功0')
                last_id1 = cursor.lastrowid


                # 插入 img 数据库
                for pic in pics:
                    url = pic['lazyload-img'][2:]
                    sql = "INSERT INTO tb_taobao2_img (img_url, ctime, mtime) VALUES ('{}', '{}', '{}')" \
                        .format(url, ctime, mtime)

                    # 执行sql语句
                    cursor.execute(sql)
                    # 提交到数据库执行
                    db.commit()
                    print('插入成功1')
                    last_id2 = cursor.lastrowid
                    sql2 = "INSERT INTO tb_taobao2_item_img_relation (taobao2_items_id, taobao2_img_id) VALUES ('{}','{}')" \
                        .format(last_id1, last_id2)

                    cursor.execute(sql2)
                    # 提交到数据库执行
                    db.commit()
                    print('插入成功2')
            except:
                db.rollback()
                print('插入失败')
        db.close()


if __name__ == '__main__':
    for cateid in range(1, 29):
        print(cateid, "开始_____________-----------------------------")
        get_items_by_category(cateid, 75)
    for cateid in range(30, 41):
        print(cateid, "开始_____________-----------------------------")
        get_items_by_category(cateid, 35)
    for cateid in range(42, 60):
        print(cateid, "开始_____________-----------------------------")
        get_items_by_category(cateid, 5)
