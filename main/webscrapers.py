from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import json


def ClothesFashionDaysScraper(sex, size, brand, clothes_type):
    all_items = []
    org_brand = brand

    # Setting URL Codes
    if sex == 'Man':
        sex = '%D0%9C%D1%8A%D0%B6%D0%B5'
    elif sex == 'Women':
        sex ='%D0%96%D0%B5%D0%BD%D0%B8'

    if clothes_type == 'T-shirts':
        clothes_type = '%D0%94%D1%80%D0%B5%D1%85%D0%B8-%D0%A2%D0%95%D0%9D%D0%98%D0%A1%D0%9A%D0%98'
    elif clothes_type == 'Hoodies':
        clothes_type = '%D0%94%D1%80%D0%B5%D1%85%D0%B8-%D0%A1%D1%83%D0%B8%D1%82%D1%88%D1%8A%D1%80%D1%82%D0%B8_%D1%81_%D0%BA%D0%B0%D1%87%D1%83%D0%BB%D0%BA%D0%B0'
    elif clothes_type == 'Tops':
        clothes_type = '%D0%94%D1%80%D0%B5%D1%85%D0%B8-%D0%91%D0%BB%D1%83%D0%B7%D0%B8'
    elif clothes_type == 'Jackets':
        clothes_type = '%D0%94%D1%80%D0%B5%D1%85%D0%B8-%D0%AF%D0%BA%D0%B5%D1%82%D0%B0'

    if brand == 'adidas':
        brand = 'adidas_performance'

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
        last_page = int(page_soup.findAll('a', {"class":"paginationLink paginationLastPage"})[0].text)

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

        for container in containers:
            original_price_container = container.findAll("span", {"class":"no-discount"})

            if (len(original_price_container) > 0):
                link = container["href"]

                original_price = original_price_container[0].text[:-6]
                original_cents = original_price_container[0].findAll("i", {"class":"price__decimals price__decimals--sup"})[0].text

                discount_price = container.findAll("strong")[0].text[:-6]
                discount_cents = container.findAll("i", {"class":"price__decimals price__decimals--sup"})[0].text
                
                picture = container.find("img", {"class":"lazy"})["data-original"]

                all_items.append({'brand': org_brand.upper(),
                                  'link': link,
                                  'pic': picture,
                                  'disc_price': float(f"{discount_price}.{discount_cents}"),
                                  'org_price': float(f"{original_price}.{original_cents}")
                                })
        page_num += 1
    return all_items


def ClothesRemixWebScraper(sex, size, brand, clothes_type):
    all_items = []
    org_brand = brand

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
    elif brand == "adidas":
        brand = "853,5610,5611,5612,33091,76789,79057,80068,86550,89433,89484,90533"
    elif brand == "napapijri":
        brand = "3831"

    size = size.upper()

    url = f'https://remixshop.com/bg/{sex}-clothes/{clothes_type}?brand={brand}&size={size}&new=1&promo=2-20,20-40,40-60,60-75,75-100'

    uClient = uReq(url)
    page_html = uClient.read()
    page_soup = soup(page_html, "html.parser")

    containers = page_soup.findAll("div", {"class":"product-box"})

    for container in containers:
        link = container.find("a", {"class":"product-photos"})["href"]

        original_price = container.find("span", {"class":"old-price"}).text.strip()[:-4]
        discount_price = container.find("span", {"class":"new-price"}).text.strip()[:-4]
        picture = container.find("img", {"class":"img-fluid"})["src"]
        
        all_items.append({'brand': org_brand.upper(),
                    'link': link,
                    'pic': picture,
                    'disc_price': float(discount_price.replace(",",".")),
                    'org_price': float(original_price.replace(",","."))
                })
    return all_items


def ClothesGlamiWebScraper(sex, size, brand, clothes_type):
    all_items = []
    org_brand = brand

    # Setting URL Codes
    if sex == "Women":
        sex ="damski"
        if clothes_type == "T-shirts":
            clothes_type = "teniski/kusi-rakavi"
        elif clothes_type == "Tops":
            clothes_type = 'teniski/dlgi-rkavi'
        elif clothes_type == "Hoodies":
            clothes_type = 'suitsrti'
        elif clothes_type == "Jackets":
            clothes_type = "iaketa-i-palta"

    if sex == "Man":
        if clothes_type == "T-shirts":
            clothes_type = "blyzi-teniski-i-flanelki/kusi-rakavi"
            sex = 'muzki'
        elif clothes_type == "Tops":
            clothes_type = 'blyzi-teniski-i-flanelki/dlgi-rkavi'
            sex = 'muzki'
        elif clothes_type == "Hoodies":
            clothes_type = 'suitsrti'
            sex = 'mzki'
        elif clothes_type == "Jackets":
            clothes_type = "aketa-i-palta"
            sex = 'mzki'

    if brand == 'adidas':
        brand = 'adidas/adidas-originals/adidas-performance'

    if size == "2XL":
        size = "xxl"
    if size == "3XL":
        return []

    uClient = uReq(f"https://www.glami.bg/{brand}/{sex}-{clothes_type}/aboutyou-bg/modivo-bg/nad-10-procenta/{size}")
    
    page_html = uClient.read()
    page_soup = soup(page_html, "html.parser")

    containers = page_soup.findAll("a", {"class":"needsclick tr-item-link j-track-ec"})

    for container in containers:
        link = container['href']

        try:
            picture = container.find("img")["data-src"]
        except:
            picture = container.find("img")["src"]

        discount_price = container.find("span", {"class":"item-price__new"}).text[:-3]
        original_price = container.find("strike", {"class":"item__price__old"}).text[:-3]

        all_items.append({'brand': org_brand.upper(),
                'link': link,
                'pic': picture,
                'disc_price': float(discount_price.replace(",",".")),
                'org_price': float(original_price.replace(",",".")),
            })
    return all_items

def ClothesSportDepotWebScraper(sex, size, brand):
    all_items = []
    org_brand = brand

    # Setting URL Codes
    if sex == "Man":
        sex = 'muje'
    elif sex == "Women":
        sex ="jeni"

    if clothes_type == 'T-shirts':
        clothes_type == 'teniski_i_potnici-2_35_103'
    elif clothes_type == 'Hoodies':
        clothes_type = 'suitsharti_i_gornishta-2_35_102'
    elif clothes_type == 'Tops':
        clothes_type == 'bluzi-2_35_1'
    elif clothes_type == 'Jackets':
        clothes_type == 'yaketa-2_35_6'

    if brand == 'adidas':
        brand = 'adidas?promotion=1&brandId=7'

    if size == 'S':
        size = '104'
    elif size == 'M':
        size = '103'
    elif size == 'L':
        size = '107'
    elif size == 'XL':
        size = '105'
    elif size == '2XL':
        size = '109'
    elif size == '3XL':
        size = '124'

    url = f"https://www.sportdepot.bg/{sex}-obleklo/{clothes_type}/{brand}&size={size}&orderBy=default&showBy=200"

    uClient = uReq(url)
    page_html = uClient.read()
    page_soup = soup(page_html, "html.parser")

    containers = page_soup.findAll("div", {"class":"col-6 col-sm-4 col-md-3 col-lg-3"})

    for container in containers:
        link_raw = container.find('a', {"class":"image"})['href']
        link = f"https://www.sportdepot.bg{link_raw}"
        
        picture_raw = container.find('a', {"class":"image"})
        picture = picture_raw.find('img')['data-src']
        
        original_price = container.find('span', {"class":"old"}).text[:-5]
        discount_price = container.find('span', {"class":"current"}).text[:-5]

        all_items.append({'brand': org_brand.upper(),
        'link': link,
        'pic': picture,
        'disc_price': float(discount_price.replace(",",".")),
        'org_price': float(original_price.replace(",",".")),
        })
    return all_items


def ShoesGlamiWebScraper(sex, size, brand):
    all_items = []
    org_brand = brand

    # Setting URL Codes
    if sex == 'Women':
        sex ='damski'
    elif sex == 'Man':
        sex = 'mzki'

    if brand == 'adidas':
        brand = 'adidas/adidas-consortium/adidas-originals/adidas-performance'
    if brand == 'nike':
        brand = 'nike/nike-performance/nike-sportswear'

    if size == '45':
        size = 'eu-45/eu-45-1_3/eu-45.5/'
    if size == '46':
        size = 'eu-46/eu-46-2_3/eu-46.5/'
    if size == '47':
        size = 'eu-47/eu-47-1_3/eu-47-2_3/eu-47.5/'

    uClient = uReq(f"https://www.glami.bg/{brand}/{sex}-obuvki/aboutyou-bg/answear-bg/bibloo-bg/footshop-bg/gomez-bg/obuvki-bg/remixshop-com/nad-10-procenta/{size}?o=2")
    page_html = uClient.read()
    page_soup = soup(page_html, "html.parser")

    containers = page_soup.findAll("a", {"class":"needsclick tr-item-link j-track-ec"})

    for container in containers:
        link = container['href']

        try:
            picture = container.find("img")["data-src"]
        except:
            picture = container.find("img")["src"]

        try:
            discount_price = container.find("span", {"class":"item-price__new"}).text[:-3]
            original_price = container.find("strike", {"class":"item__price__old"}).text[:-3]
        except:
            pass

        all_items.append({'brand': org_brand.upper(),
                'link': link,
                'pic': picture,
                'disc_price': float(discount_price.replace(",",".")),
                'org_price': float(original_price.replace(",",".")),
            })
    return all_items

def ShoesSportDepotWebScraper(sex, size, brand):
    all_items = []
    org_brand = brand

    # Setting URL Codes
    if sex == "Man":
        sex = 'muje'
    elif sex == "Women":
        sex ="jeni"

    if brand == 'adidas':
        brand = 'adidas?promotion=1&brandId=7'
    elif brand == 'nike':
        brand = 'nike?promotion=1&brandId=136'

    if size == '45':
        size = '37.64'
    elif size == '46':
        size = '38.302.65'
    elif size == '47':
        size = '80.69.95'

    url = f"https://www.sportdepot.bg/{sex}-obuvki/{brand}&size={size}&orderBy=default&showBy=200"

    uClient = uReq(url)
    page_html = uClient.read()
    page_soup = soup(page_html, "html.parser")

    containers = page_soup.findAll("div", {"class":"col-6 col-sm-4 col-md-3 col-lg-3"})

    for container in containers:
        link_raw = container.find('a', {"class":"image"})['href']
        link = f"https://www.sportdepot.bg{link_raw}"
        
        picture_raw = container.find('a', {"class":"image"})
        picture = picture_raw.find('img')['data-src']
        
        original_price = container.find('span', {"class":"old"}).text[:-5]
        discount_price = container.find('span', {"class":"current"}).text[:-5]

        all_items.append({'brand': org_brand.upper(),
        'link': link,
        'pic': picture,
        'disc_price': float(discount_price.replace(",",".")),
        'org_price': float(original_price.replace(",",".")),
        })
    return all_items