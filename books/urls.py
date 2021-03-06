"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import patterns, include, url

urlpatterns = patterns('books.views',
	url(r'^$', 'index', name = 'index'),
    url(r'^nav$', 'navigation', name = 'navigation'),
	url(r'^all-books$', 'all_books', name = 'all_books'),
	url(r'^list$', 'list'),
    url(r'^login$', 'login'),
    url(r'^logout$', 'logout'),
    url(r'^register$', 'register'),
    url(r'^list_submit$', 'list_submit'),
    url(r'^edit_list$', 'edit_list'),
    url(r'^listings-for-book/(?P<match_isbn>[-\w\ ]+)/(?P<match_title>[-\w\ ]+)', 'get_listings_for_book' ),
    url(r'^buy-book/listing/(?P<listing_id>[-\w\ ])', 'buy_book'),
    url(r'^bid-for-book/listing/(?P<listing_id>[-\w\ ]+)', 'get_bid_info'),
    url(r'^bid-for-book/bid-made/(?P<listing_id>[-\w\ ]+)', 'edit_bid'),
    url(r'^add-book$', 'book'),
    #url(r'^redirect$', 'redirect'),


	)

