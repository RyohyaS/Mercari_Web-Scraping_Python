from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_binary
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

item_ls = []
item_url_ls = []

# ブラウザの設定
options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# ブラウザの起動
browser = webdriver.Chrome(options=options)
browser.implicitly_wait(3)

# キーワード設定
KEYWORD = "macbook pro 13inch i5 16gb 256gb 2020"
MAX_ITEMS = 1000

def get_url():
    # 売り切れのみ表示&除外キーワード&ページトークン
    url = 'https://jp.mercari.com/search?keyword=' + KEYWORD + '&status=sold_out%7Ctrading&exclude_keyword=2012%2C%202013%2C%202014%2C%202015%2C%202016%2C%202017%2C%202018&page_token=v1%3A2'
    browser.get(url)
    browser.implicitly_wait(5)

    # 商品の詳細ページのURLを取得する
    item_box = browser.find_elements(By.CSS_SELECTOR, '#item-grid > ul > li')

    # 最大1件のページだけ取得する
    for i, item_elem in enumerate(item_box):
        if i >= MAX_ITEMS:
            break
        item_url_ls.append(item_elem.find_element(By.CSS_SELECTOR, 'a').get_attribute('href'))

def get_data():
    # 商品情報の詳細を取得する
    for item_url in item_url_ls:
        browser.get(item_url)
        time.sleep(3)

        # shopsのページかどうかを判定する
        shops = ("shops" in item_url)

        if shops:  # コロンを追加
            # shopsのページの場合は、それより下のコードを実行する

            # 商品名
            item_name = browser.find_element(By.CSS_SELECTOR, '.heading__a7d91561.page__a7d91561').text
            #商品説明
            item_ex = browser.find_element(By.CSS_SELECTOR, "pre[class='merText body__5616e150 primary__5616e150']").text
            #画像取得
            src = browser.find_element(By.CSS_SELECTOR, "#main > article > div.sc-a6b7d8a7-2.WrJQp > section > div > div > div > div > div.sc-a6b7d8a7-2.ishIRQ > div.sc-e76b9217-0.vYGhZ > div.slick-slider.slick-initialized > div.slick-list > div > div.slick-slide.slick-active.slick-current > div > div > div > div > figure > div.imageContainer__f8ddf3a2 > picture > img").get_attribute('src')
            #値段取得
            item_price = browser.find_element(By.CSS_SELECTOR, "#product-info > section:nth-child(1) > section:nth-child(2) > div > div > span:nth-child(2)").text
            # 出品者の名前
            owner_name = browser.find_element(By.CSS_SELECTOR, "p[class='merText body__5616e150 primary__5616e150 bold__5616e150']").text

            data = {
                '商品名': item_name,
                '商品説明': item_ex,
                '価格': item_price,
                'URL': item_url,
                '画像URL': src,
                '出品者': owner_name,
            }
            item_ls.append(data)
            
        else:
            # 商品名
            item_name = browser.find_element(By.CSS_SELECTOR, '#item-info > section:nth-child(1) > div.mer-spacing-b-12 > div > div > h1').text
            #商品説明
            item_ex = browser.find_element(By.CSS_SELECTOR, '#item-info > section:nth-child(2) > div.merShowMore.mer-spacing-b-16 > div > pre').text
            #画像取得
            src = browser.find_element(By.CSS_SELECTOR, '#main > article > div.sc-a6b7d8a7-2.WrJQp > section > div > div > div > div > div.sc-a6b7d8a7-2.ishIRQ > div > div.slick-slider.slick-initialized > div.slick-list > div > div.slick-slide.slick-active.slick-current > div > div > div > div > figure > div.imageContainer__f8ddf3a2 > picture > img').get_attribute('src')
            #値段取得
            item_price = browser.find_element(By.CSS_SELECTOR, '#item-info > section:nth-child(1) > section:nth-child(2) > div > div > span:nth-child(2)').text
            # 出品者の名前
            owner_name = browser.find_element(By.CSS_SELECTOR, 'p[class="merText body__5616e150 primary__5616e150 bold__5616e150"]').text

            data = {
                '商品名': item_name,
                '商品説明': item_ex,
                '価格': item_price,
                'URL': item_url,
                '画像URL': src,
                '出品者': owner_name,
            }
            item_ls.append(data)


def main():
    get_url()
    get_data()
    pd.DataFrame(item_ls).to_csv('メルカリデータ.csv')

if __name__ == '__main__':
    main()
