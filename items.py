# -*- coding: utf-8 -*-
import time

from bs4 import BeautifulSoup
import requests
import pymysql


def get_items_by_category(category_id=None, query=None, page_number=None):
    try:
        db = pymysql.connect("localhost", "root", "", "taobao")
        cursor = db.cursor()

        # 按页查询
        for page in range(1, page_number):
            time.sleep(2)
            print("第%s页begin--" % page)
            search_url = "https://s.2.taobao.com/list/?q=%s&search_type=item&_input_charset=utf8&catid=%s&page=%s" % (query, category_id, page)
            search_result = requests.get(search_url).content
            soup = BeautifulSoup(search_result, features="html.parser")
            divs = soup.find_all(attrs={"class": "ks-waterfall", "data-spm": "2007.1000337.16"})
            for div in divs:
                username = div.find(attrs={"class": "seller-nick"}).text[:-1]
                userpage_url = div.a['href'][2:]
                user_avatar = "wwc.alicdn.com/avatar/getAvatar.do?userNick="+username+"&type=sns"
                try:
                    user_level = div.find_all('span')[1]['title']
                except:
                    user_level = "none"

                # 商品信息
                item_info = div.find_all('a')[2]
                item_url = item_info['href'][2:]
                item_id = item_url.split("=")[1]

                # 去重
                sql = "SELECT 1 FROM tb_taobao_items_info WHERE item_id='%s' " % item_id
                cursor.execute(sql)
                item = cursor.fetchone()
                if item:
                    continue

                item_title = item_info['title'].replace("'", "''")
                item_image = item_info.find('img')['data-ks-lazyload-custom'][2:]
                item_info2 = div.find(attrs={"class": "item-attributes"})
                item_price = item_info2.find('em').text
                item_location = item_info2.find(attrs={"class": "item-location"}).text
                item_desc = div.find(attrs={"class": "item-brief-desc"}).text.replace("'", "''")

                # 时间设为当前时间（TODO）
                t = time.time()
                ctime = int(t)
                mtime = ctime

                # 插入 item 数据库
                sql = "INSERT INTO tb_taobao_items_info (username, userpage_url, user_avatar, user_level, item_id, item_url," \
                      "item_title, item_image, item_price, item_location, item_desc, category_id, ctime, mtime) " \
                      "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"\
                    % (username, userpage_url, user_avatar, user_level, item_id, item_url, item_title, item_image, item_price,
                            item_location, item_desc, category_id, ctime, mtime)
                cursor.execute(sql)

                # 大图列表(TODO)
                # pics = BeautifulSoup(requests.get("https://" + item_url).content, features="html.parser").find_all(
                #     attrs={"class": "big-img"})
                # for pic in pics:
                #     img_url = pic['lazyload-img'][2:]
                #     sql = "INSERT INTO tb_taobao_img (item_id, img_url, ctime, mtime) VALUES ('{}', '{}', '{}', '{}')" \
                #         .format(item_id, img_url, ctime, mtime)
                #     cursor.execute(sql)
            print("end---")
            db.commit()
    except Exception as e:
        db.rollback()
        print(str(e))
    finally:
        db.close()

if __name__ == '__main__':
    category_list = [
        {
            "cate_id": "50100398",
            "cate_name": "手机",
            "query": "oppo",
            "filters": ["数据线", "充电线", "钢化膜", "手机壳"],
            "black_users": ["tb071229_99"]
        },
        {
            "cate_id": "50100398",
            "cate_name": "",
            "query": "iphone",
            "filters": ["数据线", "充电线", "钢化膜", "手机壳"],
            "black_users": ["tb071229_99"]
        },
    ]
    while True:
        for category in category_list:
            get_items_by_category(category_id=category["cate_id"], query=category["query"], page_number=100)
        time.sleep(60)

