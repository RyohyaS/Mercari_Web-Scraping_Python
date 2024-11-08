from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_binary
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from selenium.common.exceptions import NoSuchElementException

item_ls = []
item_url_ls = []

# ブa
options = webdriver.ChromeOptions()
options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
#options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# ブラウザの起動
browser = webdriver.Chrome(options=options)
browser.implicitly_wait(3)

# キーワード設定
KEYWORD = input("検索キーワードを入力してください: ")
MAX_ITEMS = 1000

def get_url():
    url = 'https://jp.mercari.com/search?keyword=' + KEYWORD + '&status=sold_out%7Ctrading&exclude_keyword=2012%2C%202013%2C%202014%2C%202015%2C%202016%2C%202017%2C%202018&page_token=v1%3A2'
    browser.get(url)
    browser.implicitly_wait(5)

    # すべてのアイテムを取得
    item_boxes = browser.find_elements(By.CSS_SELECTOR, '#item-grid > ul > li')

    for i, item_elem in enumerate(item_boxes):
        if i >= MAX_ITEMS:
            break
        # アイテムのリンクを取得
        link_elements = item_elem.find_elements(By.CSS_SELECTOR, 'div > a')
        if link_elements:
            item_url = link_elements[0].get_attribute('href')
            item_url_ls.append(item_url)
            print(f"アイテム {i + 1} のリンクが見つかりました: {item_url}")
            print("スクロールします。")
            browser.execute_script("window.scrollBy(0, 100);")  # 1000px スクロール
            time.sleep(0.05)  # スクロール後の待機
        else:
            print(f"アイテム {i + 1} にリンクが見つかりませんでした。")


def get_data():
    # 商品情報の詳細を取得する
    for index, item_url in enumerate(item_url_ls, start=1):
        browser.get(item_url)
        time.sleep(3)

        # shopsのページかどうかを判定する
        shops = ("shops" in item_url)

        if shops:
            # shopsのページの場合の処理

            # 商品名
            item_name = browser.find_element(By.CSS_SELECTOR, '#product-info > section:nth-child(1) > div.mer-spacing-b-12 > div > div > h1').text
            # 商品説明
            item_ex = browser.find_element(By.CSS_SELECTOR, "#product-info > section:nth-child(2) > div.merShowMore.mer-spacing-b-16 > div > pre").text
            # 画像取得
            src = browser.find_element(By.CSS_SELECTOR, "#main > article > div.sc-1a095b48-2.dIrBJb > section > div > div > div > div > div.sc-1a095b48-2.bhLroK > div.sc-ab077df9-0.dvoZKC > div.slick-slider.slick-initialized > div.slick-list > div > div.slick-slide.slick-active.slick-current > div > div > div > div > figure > div.imageContainer__f8ddf3a2 > picture > img").get_attribute('src')
            # 値段取得
            item_price = browser.find_element(By.CSS_SELECTOR, "#product-info > section:nth-child(1) > section:nth-child(2) > div > div > span:nth-child(2)").text
            # 出品者の名前
            owner_name = browser.find_element(By.CSS_SELECTOR, "#product-info > section:nth-child(4) > div.merListItem.withArrow__884ec505.hover__884ec505.sc-604b51a1-0.ildGFv.mer-spacing-b-4 > div.content__884ec505 > a > div > div > div.content__a9529387 > p").text

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
            # shops以外のページの場合の処理

            # 商品名
            item_name = browser.find_element(By.CSS_SELECTOR, '#item-info > section:nth-child(1) > div.mer-spacing-b-12 > div.merHeading.page__a7d91561.mer-spacing-b-2 > div > h1').text
            # 商品説明
            item_ex = browser.find_element(By.CSS_SELECTOR, '#item-info > section:nth-child(2) > div.merShowMore.mer-spacing-b-16 > div > pre').text
            # 画像取得
            src = browser.find_element(By.CSS_SELECTOR, '#main > article > div.sc-1a095b48-2.sc-28317b1a-0.dIrBJb.dcHAay.mer-spacing-b-32 > section > div > div > div.sc-1a095b48-2.bhLroK > div > div.slick-slider.slick-initialized > div.slick-list > div > div.slick-slide.slick-active.slick-current > div > div > div > div > figure > div.imageContainer__f8ddf3a2 > picture > img').get_attribute('src')
            # 値段取得
            item_price = browser.find_element(By.CSS_SELECTOR, '#item-info > section:nth-child(1) > section:nth-child(2) > div.sc-1a095b48-9.idbTzw.mer-spacing-b-16 > div > div > span:nth-child(2)').text
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

        # ページの処理が完了したらnページ目完了のメッセージを表示
        print(f"{index} ページ目が完了しました。")



def main():
    get_url()
    get_data()
    pd.DataFrame(item_ls).to_csv('メルカリデータ.csv')

if __name__ == '__main__':
    main()
