from django.db import models

SIZE_CHOICES = [('XL', 'xl'), 
                ('2XL', '2xl'), 
                ('3XL', '3xl')]

class Search(models.Model):
    url = models.TextField()
    size = models.CharField(max_length=4, choices=SIZE_CHOICES, default=SIZE_CHOICES[0][0])

    def __str__(self):
        return self.url

class Item(models.Model):
    title = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    link = models.CharField(max_length=300)
    pic = models.CharField(max_length=300)
    disc_price = models.CharField(max_length=10)
    org_price = models.CharField(max_length=10)

    def __str__(self):
        return self.title