from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_binary
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

item_ls = []
item_url_ls = []

# Browser settings
options = webdriver.ChromeOptions()
options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
#options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Launch browser
browser = webdriver.Chrome(options=options)
browser.implicitly_wait(3)

# Set keyword
KEYWORD = input("Please enter the search keyword: ")
MAX_ITEMS = 1000

def get_url():
    url = 'https://jp.mercari.com/search?keyword=' + KEYWORD + '&status=sold_out%7Ctrading&exclude_keyword=2012%2C%202013%2C%202014%2C%202015%2C%202016%2C%202017%2C%202018&page_token=v1%3A2'
    browser.get(url)
    browser.implicitly_wait(5)

    # Get all items
    item_boxes = browser.find_elements(By.CSS_SELECTOR, '#item-grid > ul > li')

    for i, item_elem in enumerate(item_boxes):
        if i >= MAX_ITEMS:
            break
        try:
            # Get item link
            link_elements = item_elem.find_elements(By.CSS_SELECTOR, 'div > a')
            if link_elements:
                item_url = link_elements[0].get_attribute('href')
                item_url_ls.append(item_url)
                print(f"Item {i + 1} link found: {item_url}")
                print("Scrolling.")
                browser.execute_script("window.scrollBy(0, 100);")  # Scroll 100px
                time.sleep(0.05)  # Wait after scrolling
            else:
                print(f"Item {i + 1} link not found.")
        except StaleElementReferenceException:
            print(f"StaleElementReferenceException occurred for item {i + 1}. Retrying.")
            item_boxes = browser.find_elements(By.CSS_SELECTOR, '#item-grid > ul > li')
            item_elem = item_boxes[i]
            link_elements = item_elem.find_elements(By.CSS_SELECTOR, 'div > a')
            if link_elements:
                item_url = link_elements[0].get_attribute('href')
                item_url_ls.append(item_url)
                print(f"Item {i + 1} link found: {item_url}")
                print("Scrolling.")
                browser.execute_script("window.scrollBy(0, 100);")  # Scroll 100px
                time.sleep(0.05)  # Wait after scrolling
            else:
                print(f"Item {i + 1} link not found.")

def get_data():
    # Get item details
    for index, item_url in enumerate(item_url_ls, start=1):
        browser.get(item_url)
        time.sleep(3)

        # Check if the page is a shop page
        shops = ("shops" in item_url)

        if shops:
            try:
                # Item name
                item_name = browser.find_element(By.CSS_SELECTOR, '#product-info > section:nth-child(1) > div.mer-spacing-b-12 > div > div > h1').text
                # Item description
                item_ex = browser.find_element(By.CSS_SELECTOR, "#product-info > section:nth-child(2) > div.merShowMore.mer-spacing-b-16 > div > pre").text
                # Get image
                src = browser.find_element(By.CSS_SELECTOR, "#main > article > div.sc-1a095b48-2.dIrBJb > section > div > div > div > div > div.sc-1a095b48-2.bhLroK > div.sc-ab077df9-0.dvoZKC > div.slick-slider.slick-initialized > div.slick-list > div > div.slick-slide.slick-active.slick-current > div > div > div > div > figure > div.imageContainer__f8ddf3a2 > picture > img").get_attribute('src')
                # Get price
                item_price = browser.find_element(By.CSS_SELECTOR, "#product-info > section:nth-child(1) > section:nth-child(2) > div > div > span:nth-child(2)").text
                # Seller name
                owner_name = browser.find_element(By.CSS_SELECTOR, "#product-info > section:nth-child(4) > div.merListItem.withArrow__884ec505.hover__884ec505.sc-604b51a1-0.ildGFv.mer-spacing-b-4 > div.content__884ec505 > a > div > div > div.content__a9529387 > p").text

<<<<<<< HEAD
                data = {
                    'Item Name': item_name,
                    'Description': item_ex,
                    'Price': item_price,
                    'URL': item_url,
                    'Image URL': src,
                    'Seller': owner_name,
                }
                item_ls.append(data)
            except NoSuchElementException as e:
                print(f"Element not found: {e}")
            
        else:
            try:
                # Item name
                item_name = browser.find_element(By.CSS_SELECTOR, '#item-info > section:nth-child(1) > div.mer-spacing-b-12 > div.merHeading.page__a7d91561.mer-spacing-b-2 > div > h1').text
                # Item description
                item_ex = browser.find_element(By.CSS_SELECTOR, '#item-info > section:nth-child(2) > div.merShowMore.mer-spacing-b-16 > div > pre').text
                # Get image
                src = browser.find_element(By.CSS_SELECTOR, '#main > article > div.sc-1a095b48-2.sc-596cdc43-0.dIrBJb.eJBMGm.mer-spacing-b-32 > section > div.sc-2b7f1864-1.gASbLE > div > div.sc-1a095b48-2.bhLroK > div > div.slick-slider.slick-initialized > div.slick-list > div > div.slick-slide.slick-active.slick-current > div > div > div > div > figure > div.imageContainer__f8ddf3a2 > picture > img').get_attribute('src')
                # Get price
                item_price = browser.find_element(By.CSS_SELECTOR, '#item-info > section:nth-child(1) > section:nth-child(2) > div > div > div > span:nth-child(2)').text
                # Seller name
                owner_name = browser.find_element(By.CSS_SELECTOR, "p[class='merText body__5616e150 primary__5616e150 bold__5616e150']").text
=======
            # Product name (found using CSS selector)
            item_name = browser.find_element(By.CSS_SELECTOR, '#product-info > section:nth-child(1) > div.mer-spacing-b-12 > div > div > h1').text
            # Product information
            item_ex = browser.find_element(By.CSS_SELECTOR, "#product-info > section:nth-child(2) > div.merShowMore.mer-spacing-b-16 > div > pre").text
            # Product image
            src = browser.find_element(By.CSS_SELECTOR, "#main > article > div.sc-1a095b48-2.dIrBJb > section > div > div > div > div > div.sc-1a095b48-2.bhLroK > div.sc-ab077df9-0.dvoZKC > div.slick-slider.slick-initialized > div.slick-list > div > div.slick-slide.slick-active.slick-current > div > div > div > div > figure > div.imageContainer__f8ddf3a2 > picture > img").get_attribute('src')
            # Product Price
            item_price = browser.find_element(By.CSS_SELECTOR, "#product-info > section:nth-child(1) > section:nth-child(2) > div > div > span:nth-child(2)").text
            # Producer Name
            owner_name = browser.find_element(By.CSS_SELECTOR, "#product-info > section:nth-child(4) > div.merListItem.withArrow__884ec505.hover__884ec505.sc-604b51a1-0.ildGFv.mer-spacing-b-4 > div.content__884ec505 > a > div > div > div.content__a9529387 > p").text

            #Product split for informtion
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
            # When not in shops page

            # Product name
            item_name = browser.find_element(By.CSS_SELECTOR, '#item-info > section:nth-child(1) > div.mer-spacing-b-12 > div.merHeading.page__a7d91561.mer-spacing-b-2 > div > h1').text
            # Product Information
            item_ex = browser.find_element(By.CSS_SELECTOR, '#item-info > section:nth-child(2) > div.merShowMore.mer-spacing-b-16 > div > pre').text
            # Product Image
            src = browser.find_element(By.CSS_SELECTOR, '#main > article > div.sc-1a095b48-2.sc-28317b1a-0.dIrBJb.dcHAay.mer-spacing-b-32 > section > div > div > div.sc-1a095b48-2.bhLroK > div > div.slick-slider.slick-initialized > div.slick-list > div > div.slick-slide.slick-active.slick-current > div > div > div > div > figure > div.imageContainer__f8ddf3a2 > picture > img').get_attribute('src')
            # Product Price
            item_price = browser.find_element(By.CSS_SELECTOR, '#item-info > section:nth-child(1) > section:nth-child(2) > div.sc-1a095b48-9.idbTzw.mer-spacing-b-16 > div > div > span:nth-child(2)').text
            # Producer name
            owner_name = browser.find_element(By.CSS_SELECTOR, "p[class='merText body__5616e150 primary__5616e150 bold__5616e150']").text

            #Product split for informatioon
            data = {
                '商品名': item_name,
                '商品説明': item_ex,
                '価格': item_price,
                'URL': item_url,
                '画像URL': src,
                '出品者': owner_name,
            }
            item_ls.append(data)

        # When the page processing is complete, display a message saying "Page n completed."
        print(f"{index} page completed")
>>>>>>> 770c65dfd0484d27ef90eb6b678b5017ca6a4f18

                data = {
                    'Item Name': item_name,
                    'Description': item_ex,
                    'Price': item_price,
                    'URL': item_url,
                    'Image URL': src,
                    'Seller': owner_name,
                }
                item_ls.append(data)
            except NoSuchElementException as e:
                print(f"Element not found: {e}")

<<<<<<< HEAD
        # Display message when page processing is complete
        print(f"Page {index} completed.")

=======
# ,main databse -> items found listed onto 'mercari_data.csv'
>>>>>>> 770c65dfd0484d27ef90eb6b678b5017ca6a4f18
def main():
    get_url()
    get_data()
    pd.DataFrame(item_ls).to_csv('Mercari_Data.csv')

if __name__ == '__main__':
    main()
