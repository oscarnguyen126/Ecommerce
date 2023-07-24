from django.db import models
from users.models import User


class Cart(models.Model):
    status = models.IntegerField(default=0)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
    )

    def __str__(self):
        return self.status


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    quantity = models.IntegerField()
    cart = models.ManyToManyField(Cart)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.name
