from django.db import models
from django.utils.encoding import force_bytes

SIZE_CHOICES = [('S', 's'),
                ('M', 'm'),
                ('L', 'l'),
                ('XL', 'xl'), 
                ('2XL', '2xl'), 
                ('3XL', '3xl')]

SEX_CHOICES = [('%D0%9C%D1%8A%D0%B6%D0%B5', 'МЪЖЕ'),
               ("%D0%96%D0%B5%D0%BD%D0%B8", 'ЖЕНИ')]

# Using the URL codes
CHOTLES_TYPE = [('%D0%94%D1%80%D0%B5%D1%85%D0%B8-%D0%A2%D0%95%D0%9D%D0%98%D0%A1%D0%9A%D0%98', 'Тениски'),
              ('%D0%94%D1%80%D0%B5%D1%85%D0%B8-%D0%A1%D1%83%D0%B8%D1%82%D1%88%D1%8A%D1%80%D1%82%D0%B8_%D1%81_%D0%BA%D0%B0%D1%87%D1%83%D0%BB%D0%BA%D0%B0', 'Суитшърти'),
              ('%D0%94%D1%80%D0%B5%D1%85%D0%B8-%D0%91%D0%BB%D1%83%D0%B7%D0%B8', 'Блузи'),
              ('%D0%94%D1%80%D0%B5%D1%85%D0%B8-%D0%AF%D0%BA%D0%B5%D1%82%D0%B0', 'Якета')]

BRANDS_CHOICES = [('superdry', 'Superdry'),
                  ('diesel', 'Diesel'),
                  ('napapijri', 'Napapijri')]

class Search(models.Model):
    sex = models.CharField(max_length=50, choices=SEX_CHOICES, default=SIZE_CHOICES[0][0])
    size = models.CharField(max_length=50, choices=SIZE_CHOICES, default=SIZE_CHOICES[0][0])
    brand = models.CharField(max_length=50, choices=BRANDS_CHOICES, default=BRANDS_CHOICES[0][0])
    clothes_type = models.CharField(max_length=500, choices=CHOTLES_TYPE, default=CHOTLES_TYPE[0][0])

    def __str__(self):
        return self.url

class Item(models.Model):
    title = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    link = models.CharField(max_length=300)
    pic = models.CharField(max_length=300)
    disc_price = models.FloatField(max_length=10)
    org_price = models.FloatField(max_length=10)

    def __str__(self):
        return self.title
