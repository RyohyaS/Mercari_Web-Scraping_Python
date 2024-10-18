from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import chromedriver_binary
import time
import pandas as pd

item_ls = []
item_url_ls=[]

#ブラウザの設定
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

#ブラウザの起動
browser = webdriver.Chrome('chromedriver',options=options)
browser.implicitly_wait(3)

#キーワード設定
KEYWORD = '白Tシャツ メンズ'

def get_url():
    #売り切れ表示
    url = 'https://jp.mercari.com/search?keyword=' + KEYWORD + '&status=sold_out%7Ctrading'
    browser.get(url)
    browser.implicitly_wait(5)

    #商品の詳細ページのURLを取得する
    item_box = browser.find_elements_by_css_selector('#item-grid > ul > li')
    for item_elem in item_box:
        item_url_ls.append(item_elem.find_element_by_css_selector('a').get_attribute('href'))

def get_data():
    #商品情報の詳細を取得する
    for item_url in item_url_ls:
        browser.get(item_url)
        time.sleep(3)
        #商品名 
        item_name = browser.find_element(By.CSS_SELECTOR,'#item-info > section:nth-child(1) > div.mer-spacing-b-12 > mer-heading').text
        shadow_root = browser.find_element(By.CSS_SELECTOR,'#item-info > section:nth-child(2) > mer-show-more').shadow_root
        item_ex = shadow_root.find_element(By.CSS_SELECTOR,'div.content.clamp').text
        src_shadow = browser.find_element(By.CSS_SELECTOR,'#main > article > div.layout__LayoutCol-sc-1lyi7xi-2.jNCCiQ > section > div > div > div > div > div.layout__LayoutCol-sc-1lyi7xi-2.cHKFjh > div > div > div > div > div.slick-slide.slick-active.slick-current > div > div > mer-item-thumbnail').shadow_root
        src = src_shadow.find_element(By.CSS_SELECTOR,'div > figure > div.image-container > picture > img').get_attribute('src')
        shadow_root1 = browser.find_element_by_css_selector('#item-grid > ul > li:nth-child(1) > a > mer-item-thumbnail').shadow_root
        price_shadow = shadow_root1.find_element(By.CSS_SELECTOR,'div > figure > div.price-container > mer-price').shadow_root
        item_price = price_shadow.find_element(By.CSS_SELECTOR,'span.number').text
        
        data = {
            '商品名':item_name,
            '商品説明':item_ex,
            '価格':item_price,
            'URL':item_url,
            '画像URL':src
        }

        item_ls.append(data)


def main():
    get_url()
    get_data()
    pd.DataFrame(item_ls).to_csv('メルカリデータ.csv')


if __name__ == '__main__':
    main()
