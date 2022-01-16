from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
# Create your models here.


class User(AbstractUser):
    pass


class Products(models.Model):
    seller = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="seller_name")
    product_name = models.TextField()
    price = models.FloatField()

    class Meta:
        ordering = ('price',)
  
    def __str__(self):
        return f"{self.id}: {self.seller} is Selling {self.product_name} for {self.price}"
