from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import json
import math
import re


def ClothesFashionDaysScraper(sex, size, brand, clothes_type):
    all_items = []
    org_brand = brand
    org_clothes = clothes_type

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
    elif clothes_type == 'Pants':
        clothes_type = '%D0%94%D1%80%D0%B5%D1%85%D0%B8-%D0%9F%D0%B0%D0%BD%D1%82%D0%B0%D0%BB%D0%BE%D0%BD%D0%B8'

    if brand == 'adidas':
        brand = 'adidas_originals+adidas_performance'

    page_num = 1
    last_page = 1

    base_url = f'https://www.fashiondays.bg/g/{sex}-{brand}/{clothes_type}'

    if org_clothes == 'Pants':
        sizes_url = f'size[69__{size.lower()}]=69__{size.lower()}'
    else:
        sizes_url = f'size[70__{size.lower()}]=70__{size.lower()}'

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
    elif clothes_type == "Pants":
        clothes_type = 'trousers'
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
        elif clothes_type == "Pants":
            return []

    if brand == 'adidas':
        brand = 'adidas/adidas-originals/adidas-performance'

    if size == "2XL":
        size = "xxl"
    if size == "3XL":
        return []

    url = f"https://www.glami.bg/{brand}/{sex}-{clothes_type}/aboutyou-bg/answear-bg/bibloo-bg/modivo-bg/nad-10-procenta/{size.lower()}"
    uClient = uReq(url)
    
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

def ClothesSportDepotWebScraper(sex, size, brand, clothes_type):
    all_items = []
    org_brand = brand

    # Setting URL Codes
    if sex == "Man":
        sex = 'muje'
    elif sex == "Women":
        sex ="jeni"

    if clothes_type == 'T-shirts':
        clothes_type = 'teniski_i_potnici-2_35_103'
    elif clothes_type == 'Hoodies':
        clothes_type = 'suitsharti_i_gornishta-2_35_102'
    elif clothes_type == 'Tops':
        clothes_type = 'bluzi-2_35_1'
    elif clothes_type == 'Jackets':
        clothes_type = 'yaketa-2_35_6'
    elif clothes_type == 'Pants':
        clothes_type = 'pantaloni-2_35_2'

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
        brand = 'air-jordan-nike/nike/nike-performance/nike-sportswear'

    if size == '36':
        size = 'eu-36/eu-36-1_3/eu-36-2_3/eu-36.5/'
    elif size == '37':
        size = 'eu-37/eu-37-1_3/eu-37-2_3/eu-37.5/'
    elif size == '38':
        size = 'eu-38/eu-38-1_3/eu-38-2_3/eu-38.5/'
    elif size == '39':
        size = 'eu-39/eu-39-1_3/eu-39-2_3/eu-39.5/'
    elif size == '40':
        size = 'eu-40/eu-40-1_3/eu-40-2_3/eu-40.5/'
    elif size == '41':
        size = 'eu-41/eu-41-1_3/eu-41-2_3/eu-41.5/'
    elif size == '42':
        size = 'eu-42/eu-42-1_3/eu-42-2_3/eu-42.5/'
    elif size == '43':
        size = 'eu-43/eu-43-1_3/eu-43-2_3/eu-43.5/'
    elif size == '44':
        size = 'eu-44/eu-44-1_3/eu-44-2_3/eu-44.5/'
    elif size == '45':
        size = 'eu-45/eu-45-1_3/eu-45-2_3/eu-45.5/'
    elif size == '46':
        size = 'eu-46/eu-46-1_3/eu-46-2_3/eu-46.5/'
    elif size == '47':
        size = 'eu-47/eu-47-1_3/eu-47-2_3/eu-47.5/'
    elif size == '48':
        size = 'eu-48/eu-48-1_3/eu-48-2_3/eu-48.5/'

    url = f"https://www.glami.bg/{brand}/{sex}-obuvki/aboutyou-bg/bibloo-bg/footshop-bg/modivo-bg/obuvki-bg/answear-bg/nad-10-procenta/{size}?o=2"
    print(url)
    uClient = uReq(url)
    page_html = uClient.read()
    page_soup = soup(page_html, "html.parser")

    # Finding the number of pages
    items_num_text = page_soup.find("div", {"class","header__description"}).text[:-20]
    items_num = int(re.findall("\d+", items_num_text)[0])
    pages_num = math.ceil(items_num / 120)
    
    for page in range(1, pages_num+1):
        url = f"https://www.glami.bg/{brand}/{sex}-obuvki/aboutyou-bg/bibloo-bg/footshop-bg/modivo-bg/obuvki-bg/remixshop-com/answear-bg/nad-10-procenta/{size}?p={page}&o=2"
        uClient = uReq(url)
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
        brand = 'nike,jordan?promotion=1&brandId=136.435'

    if size == '36':
        size = '48.70'
    elif size == '37':
        size = '39.81.46'
    elif size == '38':
        size = '40.89.59.477'
    elif size == '39':
        size = '50.58.57.474'
    elif size == '40':
        size = '474.49.90.60'
    elif size == '41':
        size = '34.325.204.475'
    elif size == '42':
        size = '475.35.33.63'
    elif size == '43':
        size = '36.66.98.487'
    elif size == '44':
        size = '487.41.82.67'
    elif size == '45':
        size = '37.64.87.499'
    elif size == '46':
        size = '499.38.302.65'
    elif size == '47':
        size = '80.69.95'
    elif size == '48':
        size = '72.92'
    
    url = f"https://www.sportdepot.bg/{sex}-obuvki/{brand}&size={size}&orderBy=default&showBy=200"
    uClient = uReq(url)
    page_html = uClient.read()
    page_soup = soup(page_html, "html.parser")
    none_found = page_soup.find('span', {'class':'page-result-count text-gray text-sm'}).text[:-21]
    if int(none_found) > 300:
        return []

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