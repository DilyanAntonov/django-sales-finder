from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

import json

def FashionDaysScraper(sex, size, brand, clothes_type):
    all_items = []
    page_num = 1
    last_page = 1

    base_url = f'https://www.fashiondays.bg/g/{sex}-{brand}/{clothes_type}'
    sizes_url = f'size[70__{size}]=70__{size}'

    joined_url = f'{base_url}?{sizes_url}'

    uClient = uReq(joined_url)

    many_pages = False

    # Check if page is not found
    page_html = uClient.read()
    page_soup = soup(page_html, "html.parser")

    # Check if there are multiple pages
    items_count = page_soup.findAll("div", {"class":"absolute"})[0].text.replace(" ", "")[:-9]

    # Item Count
    try:
        items_count = int(items_count)
    except:
        items_count = 1

    if (items_count>90):
        many_pages = True
        last_page = int(page_soup.findAll("a", {"class":"paginationLink paginationLastPage"})[0].text)

    # Forming Size Link

    for i in range(0, last_page):
        if many_pages:
            search_url = f"{base_url}?page={page_num}&{sizes_url}"
        else:
            search_url = joined_url

        uClient = uReq(search_url)

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
                                  'disc_price': float(f"{discount_price}.{discount_cents}"),
                                  'org_price': float(f"{original_price}.{original_cents}")
                                })
        page_num += 1

    return all_items