from django.db import models

class Item(models.Model):
    title = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    link = models.CharField(max_length=300)
    pic = models.CharField(max_length=300)
    disc_price = models.CharField(max_length=10)
    org_price = models.CharField(max_length=10)

    def __str__(self):
        return self.title