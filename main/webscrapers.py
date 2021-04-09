from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import json

def FashionDaysScraper(sex, size, brand, clothes_type):

    # Setting URL Codes
    if sex == "Man":
        sex = '%D0%9C%D1%8A%D0%B6%D0%B5'
    elif sex == "Women":
        sex ="%D0%96%D0%B5%D0%BD%D0%B8"

    if clothes_type == "T-shirts":
        clothes_type = '%D0%94%D1%80%D0%B5%D1%85%D0%B8-%D0%A2%D0%95%D0%9D%D0%98%D0%A1%D0%9A%D0%98'
    elif clothes_type == "Hoodies":
        clothes_type = '%D0%94%D1%80%D0%B5%D1%85%D0%B8-%D0%A1%D1%83%D0%B8%D1%82%D1%88%D1%8A%D1%80%D1%82%D0%B8_%D1%81_%D0%BA%D0%B0%D1%87%D1%83%D0%BB%D0%BA%D0%B0'
    elif clothes_type == "Tops":
        clothes_type = '%D0%94%D1%80%D0%B5%D1%85%D0%B8-%D0%91%D0%BB%D1%83%D0%B7%D0%B8'
    elif clothes_type == "Jackets":
        clothes_type = '%D0%94%D1%80%D0%B5%D1%85%D0%B8-%D0%AF%D0%BA%D0%B5%D1%82%D0%B0'
    
    
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
            original_price_container = container.findAll("span", {"class":"no-discount"})
            if (len(original_price_container) > 0):
                brand = container.findAll("span", {"class":"brand-name"})[0].text
                link = container["href"]

                original_price = original_price_container[0].text[:-6]
                original_cents = original_price_container[0].findAll("i", {"class":"price__decimals price__decimals--sup"})[0].text

                discount_price = container.findAll("strong")[0].text[:-6]
                discount_cents = container.findAll("i", {"class":"price__decimals price__decimals--sup"})[0].text
                
                picture = container.find("img", {"class":"lazy"})["data-original"]

                all_items.append({'brand': brand,
                                  'link': link,
                                  'pic': picture,
                                  'disc_price': float(f"{discount_price}.{discount_cents}"),
                                  'org_price': float(f"{original_price}.{original_cents}")
                                })
        page_num += 1

    return all_items


def RemixWebScraper(sex, size, brand, clothes_type):

    # Setting URL Codes
    if sex == "Man":
        sex = 'mens'
    elif sex == "Women":
        sex ="womens"

    if clothes_type == "Hoodies":
        clothes_type = 'sweatshirts'
    else:
        clothes_type = clothes_type.lower()

    if brand == "superdry":
        brand = "22289"
    elif brand == "diesel":
        brand = "1116"
    elif brand == "napapijri":
        brand = "3831"

    size = size.upper()

    all_items = []

    url = f'https://remixshop.com/bg/{sex}-clothes/{clothes_type}?brand={brand}&size={size}&new=1&promo=2-20,20-40,40-60,60-75,75-100'

    uClient = uReq(url)

    page_html = uClient.read()
    page_soup = soup(page_html, "html.parser")

    containers = page_soup.findAll("div", {"class":"product-box"})

    for container in containers:
        brand = container.find("a", {"class":"product-brand"}).text.strip()
        link = container.find("a", {"class":"product-photos"})["href"]

        original_price = container.find("span", {"class":"old-price"}).text.strip()[:-4]
        discount_price = container.find("span", {"class":"new-price"}).text.strip()[:-4]
        picture = container.find("img", {"class":"img-fluid"})["src"]
        
        all_items.append({'brand': brand,
                    'link': link,
                    'pic': picture,
                    'disc_price': float(discount_price.replace(",",".")),
                    'org_price': float(original_price.replace(",",".")),
                })
    
    return all_items
