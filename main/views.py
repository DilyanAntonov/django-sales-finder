from django.shortcuts import render, redirect
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from django.forms.models import model_to_dict
from .models import Item, Search
from .forms import SearchForm
from .webscrapers import FashionDaysScraper
import json


def home(request):
    form = SearchForm()
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

    url = model_to_dict(Search.objects.filter()[0])['url']
    size = model_to_dict(Search.objects.filter()[0])['size']
   
    all_items = FashionDaysScraper(url, size)

    for item in all_items:
        product = Item()

        product.title = item['name']
        product.brand = item['brand']
        product.link = item['link']
        product.pic = item['pic']
        product.disc_price = item['disc_price']
        product.org_price = item['org_price']

        product.save()

    context = {
        'items': Item.objects.all()
    }

    Search.objects.all().delete()

    return render(request, 'main/search-results.html', context)

