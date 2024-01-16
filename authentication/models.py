from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    quantity = models.IntegerField(default=1)
    img = models.ImageField(upload_to='products/')
    model_3d = models.FileField(upload_to='models/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return self.name
