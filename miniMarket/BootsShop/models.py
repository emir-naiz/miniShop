from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class UserProfile(models.Model):
    image = models.ImageField(blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    phone = models.IntegerField()

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=200)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', args=[self.id])

class Products(models.Model):
    types = (
        ('Sneakers', 'Sneakers'),
        ('Classic', 'Classic'),
        ('High Tops', 'High Tops'),
        ('Boots', 'Boots')
    )
    genders = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Uni', 'Uni'),
    )
    sizes = (
        ('36', '36'),
        ('37', '37'),
        ('38', '38'),
        ('39', '39'),
        ('40', '40'),
        ('41', '41'),
        ('42', '42'),
        ('43', '43'),
        ('44', '44'),
    )

    image = models.ImageField(blank=True)
    name = models.CharField(max_length=40)
    product_model = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    product_type = models.CharField(max_length=40, choices=types)
    gender = models.CharField(max_length=20, choices=genders)
    size = models.CharField(max_length=20, choices=sizes)
    price = models.IntegerField()


    def __str__(self):
        return self.name + ' ' + self.product_model







