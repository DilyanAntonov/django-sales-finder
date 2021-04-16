from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from .models import Item, Search
from .forms import SearchForm
from .webscrapers import FashionDaysScraper, RemixWebScraper, GlamiWebScraper, SportDepotWebScraper
import json
import urllib


def home(request):
    form = SearchForm(use_required_attribute=False)
    Search.objects.all().delete()

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('search')

    context = {'form': form}
    return render(request, 'main/home.html', context)
 
def search(request):
    Item.objects.all().delete()

    all_items = []
    fashiondays_items = []
    remix_items = []
    glami_items = []
    sportdepot_items =[]

    sex = model_to_dict(Search.objects.filter()[0])['sex']
    size = model_to_dict(Search.objects.filter()[0])['size']
    brand = model_to_dict(Search.objects.filter()[0])['brand']
    clothes_type = model_to_dict(Search.objects.filter()[0])['clothes_type']

    try:
        fashiondays_items = FashionDaysScraper(sex, size, brand, clothes_type)
    except:
        pass

    try:
        remix_items = RemixWebScraper(sex, size, brand, clothes_type)
    except:
        pass

    try:
        glami_items = GlamiWebScraper(sex, size, brand, clothes_type)
    except:
        pass

    try:
        sportdepot_items = SportDepotWebScraper(sex, size, brand, clothes_type)
    except:
        pass

    print(len(fashiondays_items))
    print(len(remix_items))
    print(len(glami_items))
    print(len(sportdepot_items))
    
    if len(fashiondays_items) > 0:
        all_items += fashiondays_items
    if len(remix_items) > 0:
        all_items += remix_items
    if len(glami_items) > 0:
        all_items += glami_items  
    if len(sportdepot_items) > 0: 
        all_items += sportdepot_items


    for item in all_items:
        product = Item()

        product.brand = item['brand']
        product.link = item['link']
        product.pic = item['pic']
        product.disc_price = item['disc_price']
        product.org_price = item['org_price']

        product.save()

    context = {
        'items': Item.objects.order_by('disc_price').all()
    }


    return render(request, 'main/search-results.html', context)

        

