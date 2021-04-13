from django.db import models
from django.utils.encoding import force_bytes

SIZE_CHOICES = [('S', 's'),
                ('M', 'm'),
                ('L', 'l'),
                ('XL', 'xl'), 
                ('2XL', '2xl'), 
                ('3XL', '3xl')]

SEX_CHOICES = [('Man', 'МЪЖЕ'),
               ('Women', 'ЖЕНИ')]

CHOTLES_TYPE = [('T-shirts', 'Тениски'),
              ('Hoodies', 'Суитшърти'),
              ('Tops', 'Блузи'),
              ('Jackets', 'Якета')]

BRANDS_CHOICES = [('superdry', 'Superdry'),
                  ('diesel', 'Diesel'),
                  ('adidas', 'Adidas'),
                  ('napapijri', 'Napapijri')]

class Search(models.Model):
    sex = models.CharField(max_length=50, choices=SEX_CHOICES, default=SIZE_CHOICES[0][0])
    size = models.CharField(max_length=50, choices=SIZE_CHOICES, default=SIZE_CHOICES[0][0])
    brand = models.CharField(max_length=50, choices=BRANDS_CHOICES, default=BRANDS_CHOICES[0][0])
    clothes_type = models.CharField(max_length=500, choices=CHOTLES_TYPE, default=CHOTLES_TYPE[0][0])

    def __str__(self):
        return self.brand

class Item(models.Model):
    brand = models.CharField(max_length=50)
    link = models.CharField(max_length=300)
    pic = models.CharField(max_length=300)
    disc_price = models.FloatField(max_length=10)
    org_price = models.FloatField(max_length=10)

    def __str__(self):
        return self.title
