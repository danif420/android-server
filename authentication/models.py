from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    img = models.ImageField(upload_to='products/')
    model_3d = models.FileField(upload_to='models/', null=True, blank=True)

    def __str__(self):
        return self.name
