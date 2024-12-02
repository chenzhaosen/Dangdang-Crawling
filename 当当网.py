import requests
from lxml import etree
from pandas import DataFrame
1
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 获取用户输入的页数
page_size = input("请输入要获取的页数：")

# 用于存储所有书籍信息的列表
book_data = []

# 遍历每一页
for page_index in range(1, int(page_size) + 1):
    url = f'https://search.dangdang.com/?key=%C5%C0%B3%E6&act=input&page_index={page_index}'

    res = requests.get(url, headers=headers)
    html = etree.HTML(res.text)

    # 获取每个li标签，即每本书的信息
    all_li = html.xpath('//ul[@class="bigimg"]/li')

    for li in all_li:
        book_info = {}

        # 书名
        book_info['书名'] = li.xpath('./a/@title')[0]

        # 价格
        book_info['价格'] = li.xpath('./p[@class="price"]/span[1]/text()')[0]

        # 作者
        author = li.xpath('./p[@class="search_book_author"]/span[1]/a/text()')
        if author:
            book_info['作者'] = author[0]
        else:
            None

        # 出版社
        book_info['出版社'] = li.xpath('./p[@class="search_book_author"]/span[3]/a/text()')[0]

        print(book_info)

        # 将每本书的数据添加到book_data列表
        book_data.append(book_info)

# 将所有书籍信息转换为DataFrame
info = DataFrame(book_data)

# 保存到Excel文件
info.to_excel("./书籍数据.xlsx", index=False)
print("数据保存完成!!!")
