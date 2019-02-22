import requests
import json
import pymysql
import time


def make_url(page_num, category_id):
    part_one = 'https://s.2.taobao.com/list/waterfall/waterfall.htm?'
    part_two = 'wp=' + page_num
    part_three = '&_ksTS=1550133630515_142'
    part_four = '&callback=jsonp143&stype=1'
    part_five = '&catid=' + category_id
    part_six = '&st_trust=1'
    part_seven = '&ist=1'
    return part_one + part_two + part_three + part_four + part_five + part_six + part_seven


def get_page(url):
    req = requests.get(url)
    print(req.text)
    print('---------------------')
    if req.status_code != 200:
        return -1
    if len(req.text) < 100:
        return -1
    return req.text[12:-2]


def page_decoder(json_context):
    return json.loads(json_context)


def get_category(id):
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "root", "taobao2")

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    sql = "SELECT code FROM t_category WHERE id = {} LIMIT 1".format(id)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        result = cursor.fetchone()
    except:
        print("Error: unable to fetch data")

    # 关闭数据库连接
    db.close()

    return result


def get_items_by_category(cid, number):
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "root", "taobao2")

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    for num in range(1, number+1):
        # 获取到url
        cateId = "".join(get_category(cid))
        pageNum = str(num)
        url = make_url(pageNum, cateId)
        # 获取界面
        page = get_page(url)
        while page == -1:
            page = get_page(url)

        # 解析界面
        try:
            jsonContent = page_decoder(page)
            # 插入数据
            for content in jsonContent['idle']:
                imageUrl = content['item']['imageUrl'][2:]
                itemUrl = content['item']['itemUrl'][2:]
                isBrandNew = content['item']['isBrandNew']
                price = content['item']['price']
                orgPrice = content['item']['orgPrice']
                city = content['item']['provcity']
                description = content['item']['describe']
                commentCount = content['item']['commentCount']
                title = content['item']['title']
                userNick = content['user']['userNick']
                vipLevel = content['user']['vipLevel']
                isSinaV = content['user']['isSinaV']
                userItemsUrl = content['user']['userItemsUrl'][2:]
                categoryId = cid

                sql = "INSERT INTO t_items (image_url, item_url, is_brand_new, price, org_price, city, description," \
                      "comment_count, title, user_nick, vip_level, is_sina_v, user_items_url, category_id) " \
                      "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, '{}', '{}', {}, '{}', '{}', {})".format(
                    imageUrl, itemUrl, isBrandNew, price, orgPrice, city, description, commentCount, title, userNick,
                    vipLevel, isSinaV, userItemsUrl, categoryId)
                try:
                    # 执行sql语句
                    cursor.execute(sql)
                    # 提交到数据库执行
                    db.commit()
                    print(cateId, '号分类第', num, '页插入成功')
                except:
                    # 如果发生错误则回滚
                    db.rollback()
                    print('插入失败')
        except:
            print('数据解析错误')


        time.sleep(7)
    db.close()

#
#
# url = "https://s.2.taobao.com/list/waterfall/waterfall.htm?wp=2&" \
#       "_ksTS=1550133630515_142&" \
#       "callback=jsonp143&" \
#       "stype=1&" \
#       "catid=50100398&" \
#       "st_trust=1&" \
#       "ist=1"


if __name__ == '__main__':
    # 种类计数
    for cateid in range(1, 29):
        get_items_by_category(cateid, 100)
    for cateid in range(30, 41):
        get_items_by_category(cateid, 50)
    for cateid in range(42, 60):
        get_items_by_category(cateid, 5)

