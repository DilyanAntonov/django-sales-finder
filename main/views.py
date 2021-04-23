from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from .models import ClothesItem, ClothesSearch
from .models import ShoesItem, ShoesSearch
from .forms import ClothesSearchForm, ShoesSearchForm
from .webscrapers import ClothesFashionDaysScraper, ClothesRemixWebScraper, ClothesGlamiWebScraper, ClothesSportDepotWebScraper
from .webscrapers import ShoesSportDepotWebScraper, ShoesGlamiWebScraper
import json
import urllib


def home(request):
    return render(request, 'main/home.html')

def about(request):
    return render(request, 'main/about.html')

def clothes(request):
    form = ClothesSearchForm(use_required_attribute=False)
    ClothesSearch.objects.all().delete()

    if request.method == 'POST':
        form = ClothesSearchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clothes_search')

    context = {'form': form}
    return render(request, 'main/clothes/clothes-home.html', context)
 
def clothes_search(request):
    ClothesItem.objects.all().delete()

    all_items = []
    fashiondays_items = []
    remix_items = []
    glami_items = []
    sportdepot_items =[]

    sex = model_to_dict(ClothesSearch.objects.filter()[0])['sex']
    size = model_to_dict(ClothesSearch.objects.filter()[0])['size']
    brand = model_to_dict(ClothesSearch.objects.filter()[0])['brand']
    clothes_type = model_to_dict(ClothesSearch.objects.filter()[0])['clothes_type']

    try:
        fashiondays_items = ClothesFashionDaysScraper(sex, size, brand, clothes_type)
    except:
        pass
    try:
        remix_items = ClothesRemixWebScraper(sex, size, brand, clothes_type)
    except:
        pass
    try:
        glami_items = ClothesGlamiWebScraper(sex, size, brand, clothes_type)
    except:
        pass
    try:
        sportdepot_items = ClothesSportDepotWebScraper(sex, size, brand, clothes_type)
    except:
        pass
    
    if len(fashiondays_items) > 0:
        all_items += fashiondays_items
    if len(remix_items) > 0:
        all_items += remix_items
    if len(glami_items) > 0:
        all_items += glami_items  
    if len(sportdepot_items) > 0: 
        all_items += sportdepot_items

    if all_items == []:
        return render(request, 'main/notfound.html')
    else:
        for item in all_items:
            product = ClothesItem()

            product.brand = item['brand']
            product.link = item['link']
            product.pic = item['pic']
            product.disc_price = item['disc_price']
            product.org_price = item['org_price']

            product.save()

        context = {
            'items': ClothesItem.objects.order_by('disc_price').all()
        }

        return render(request, 'main/clothes/clothes-search-results.html', context)

def shoes(request):
    form = ShoesSearchForm(use_required_attribute=False)
    ShoesSearch.objects.all().delete()

    if request.method == 'POST':
        form = ShoesSearchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shoes_search')

    context = {'form': form}
    return render(request, 'main/shoes/shoes-home.html', context)


def shoes_search(request):
    ShoesItem.objects.all().delete()

    all_items = []
    sportdepot_items = []
    glami_items = []

    sex = model_to_dict(ShoesSearch.objects.filter()[0])['sex']
    size = model_to_dict(ShoesSearch.objects.filter()[0])['size']
    brand = model_to_dict(ShoesSearch.objects.filter()[0])['brand']

    try:
        sportdepot_items = ShoesSportDepotWebScraper(sex, size, brand)
    except:
        pass
    # try:
    #     glami_items = ShoesGlamiWebScraper(sex, size, brand)
    # except:
    #     pass
     
    if len(sportdepot_items) > 0: 
        all_items += sportdepot_items
    # if len(glami_items) > 0:
    #     all_items += glami_items

    if all_items == []:
        return render(request, 'main/notfound.html')
    else:
        for item in all_items:
            product = ShoesItem()

            product.brand = item['brand']
            product.link = item['link']
            product.pic = item['pic']
            product.disc_price = item['disc_price']
            product.org_price = item['org_price']

            product.save()

        context = {
            'items': ShoesItem.objects.order_by('disc_price').all()
        }

        return render(request, 'main/shoes/shoes-search-results.html', context)