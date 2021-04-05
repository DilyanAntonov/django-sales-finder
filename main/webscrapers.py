from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

import json

def FashionDaysScraper(url):
    all_items = []
    page_num = 1
    # my_url = f"{url}?page={page_num}"
    uClient = uReq(url)

    page_html = uClient.read()
    page_soup = soup(page_html, "html.parser")

    # Checks if there are multiple pages 
    # #TODO Can be done better
    items_count = int(page_soup.findAll("div", {"class":"absolute"})[0].text.replace(" ", "")[:-9])
    many_pages = False

    if (items_count>90):
        many_pages = True
        last_page = int(page_soup.findAll("a", {"class":"paginationLink paginationLastPage"})[0].text)
    else:
        last_page=1

    for i in range(0, last_page):
        my_url = my_url = f"{url}?page={page_num}"
        uClient = uReq(my_url)

        page_html = uClient.read()
        page_soup = soup(page_html, "html.parser")
            
        containers = page_soup.findAll("a", {"class":"campaign-item"})
        container = containers[0]

        for container in containers:
            brand = container.findAll("span", {"class":"brand-name"})[0].text
            link = container["href"]
            original_price_container = container.findAll("span", {"class":"no-discount"})
            if (len(original_price_container) > 0):
                original_price = original_price_container[0].text[:-6]
                original_cents = original_price_container[0].findAll("i", {"class":"price__decimals price__decimals--sup"})[0].text

                discount_price = container.findAll("strong")[0].text[:-6]
                discount_cents = container.findAll("i", {"class":"price__decimals price__decimals--sup"})[0].text
                
                name = container.findAll("span", {"class":"product-description"})[0].text
                picture = container.find("img", {"class":"lazy"})["data-original"]

                all_items.append({'name': name,
                                  'brand': brand,
                                  'link': link,
                                  'pic': picture,
                                  'disc_price': f"{discount_price}.{discount_cents}",
                                  'org_price': f"{original_price}.{original_cents}"})
        page_num += 1

    return all_items