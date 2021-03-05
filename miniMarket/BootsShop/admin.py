from django.contrib import admin
from BootsShop.models import UserProfile, Products, Category

admin.site.register([UserProfile ,Products, Category])