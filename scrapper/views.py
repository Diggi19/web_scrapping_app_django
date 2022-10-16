from django.shortcuts import render
from bs4 import BeautifulSoup
"""
    this takes a htmll file and allows us to search data present in the class and get it by classnames
"""

import requests
from requests.compat import quote_plus  # helps in automatically add %20 to spaced words in url
# e.g python on the loose  = python+on+the+loose

# db
from .models import Search

# Create your views here.
base_craiglist_url = "https://bangalore.craigslist.org/search/bbb?query={}"  # {} is important
def home(request):
    context = {
        "name":"justin ferrow"
    }
    return render(request, "base.html", context)


def new_search(request):
    """ get the searched value and concat it to baseurl """
    search = request.POST.get('search')
    #Search.objects.create(search = search) # storing searches in db
    final_url = base_craiglist_url.format(quote_plus(search))
    # print(final_url)


    """ use the final_url to get data from craiglist site"""
    response = requests.get(final_url)   # makes a request to that url
    data = response.text
    # print(data)                                                           # gets the html and css from the site

    """ getting data from the html tags using BeautifulSoup"""
    soup = BeautifulSoup(data,features = 'html.parser')   # incapsulates the html data as raw text

    # getting data
    final_posting = []
    post_listings = soup.find_all('li',{'class':'result-row'})
    # print(post_listings)

    """ setting a final posting list"""
    for post in post_listings:
            post_title = post.find(class_ = 'result-title')
            post_url = post.find('a').get('href')
            post_heading = post.find(class_ = 'result-heading')
            if post.find(class_ = 'result-price'):
                post_price = post.find(class_ = 'result-price')
            else:
                post_price ='N/A'

            """ getting image"""
            image_base_url = 'https://images.craigslist.org/{}_300x300.jpg'
            data_id = str(post.find('a').get('data-ids'))
            if data_id != 'None':
                single_id = data_id.split(",")[0]
                trimmed_id = single_id[2:len(single_id)]
                #print(trimmed_id)
                post_image = image_base_url.format(trimmed_id)
                print(post_image)
            else:
                post_image = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQrcqM6uaWmu08JahpGJ9z4q5NkosS0nvvQbQ&usqp=CAU"

            final_posting.append(
                {
                    'post_title': post_title.text,
                    'post_url' : post_url,
                    'post_price' : post_price,
                    'post_heading' : post_heading.text,
                    'post_image':post_image

                }
            )


    #print(final_posting)
    context = {
        'final_posting':final_posting,
    }
    return render(request,'scrapper/new_search.html',context)
