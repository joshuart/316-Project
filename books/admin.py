from django.contrib import admin

from .models import Seller, Book

admin.site.register(Seller)
admin.site.register(Book)