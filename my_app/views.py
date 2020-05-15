from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from . import models
from requests.compat import quote_plus
# Create your views here.
def home(request):
    return render(request,template_name='base.html')

BASE_URL="https://losangeles.craigslist.org/search/?query={}"
def new_search(request):
    search=request.POST.get('searchy')
    models.Search.objects.create(search=search)

    final_url=BASE_URL.format(quote_plus(search))
    base_image_url="https://images.craigslist.org/{}_300x300.jpg"
    #print(final_url)
    response=requests.get(final_url)
    data=response.text
    #print(data)
    soup=BeautifulSoup(data,features='html.parser')
    final_posting=[]
    post_listing=soup.find_all('li',{'class':'result-row'})
    for post in post_listing:
        post_title=post.find(class_='result-title').text
        post_link=post.find('a').get('href')
        if(post.find(class_='result-price')):
            post_price=post.find(class_='result-price').text
        else:
            post_price='N/A'
        image_link="https://bitsofco.de/content/images/2018/12/Screenshot-2018-12-16-at-21.06.29.png"
        if(post.find(class_='result-image').get('data-ids')):
            dataid=(post.find(class_='result-image').get('data-ids'))
            firstid=dataid.split(',')[0]
            image_link=base_image_url.format(firstid[2:])
        final_posting.append((post_title,post_link,post_price,image_link))

    stuff_for_frontend={'search':search,
                        'results':final_posting,
                        }
    return render(request,template_name='my_app/new_search.html',context=stuff_for_frontend)