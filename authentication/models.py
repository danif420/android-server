from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    img = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name
