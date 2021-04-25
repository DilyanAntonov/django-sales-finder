from django.db import models
from django.utils.encoding import force_bytes

SEX_CHOICES = [('Man', 'МЪЖЕ'),
               ('Women', 'ЖЕНИ')]

# Clothes Form Fields
CLOTHES_SIZE_CHOICES = [('S', 'S'),
                        ('M', 'M'),
                        ('L', 'L'),
                        ('XL', 'XL'), 
                        ('2XL', '2XL'), 
                        ('3XL', '3XL')]

CLOTHES_BRANDS_CHOICES = [('superdry', 'Superdry'),
                          ('diesel', 'Diesel'),
                          ('adidas', 'Adidas'),
                          ('nike', 'Nike'),
                          ('poloralphlauren', 'Polo Ralph Lauren'),
                          ('napapijri', 'Napapijri'),
                          ('guess', 'Guess')]

CHOTLES_TYPE = [('T-shirts', 'Тениски'),
                ('Hoodies', 'Суитшърти'),
                ('Tops', 'Блузи'),
                ('Jackets', 'Якета'),
                ('Pants', 'Долнища')]

class ClothesSearch(models.Model):
    sex = models.CharField(max_length=50, choices=SEX_CHOICES, default=SEX_CHOICES[0][0])
    size = models.CharField(max_length=50, choices=CLOTHES_SIZE_CHOICES, default=CLOTHES_SIZE_CHOICES[0][0])
    brand = models.CharField(max_length=50, choices=CLOTHES_BRANDS_CHOICES, default=CLOTHES_BRANDS_CHOICES[0][0])
    clothes_type = models.CharField(max_length=500, choices=CHOTLES_TYPE, default=CHOTLES_TYPE[0][0])

    def __str__(self):
        return self.clothes_type

class ClothesItem(models.Model):
    brand = models.CharField(max_length=50)
    link = models.CharField(max_length=300)
    pic = models.CharField(max_length=300)
    disc_price = models.FloatField(max_length=10)
    org_price = models.FloatField(max_length=10)

    def __str__(self):
        return self.brand

# Shoes Form Fields
SHOES_SIZE_CHOICES = [('36', '36'), 
                        ('37', '37'), 
                        ('38', '38'), 
                        ('39', '39'), 
                        ('40', '40'), 
                        ('41', '41'), 
                        ('42', '42'), 
                        ('43', '43'), 
                        ('44', '44'), 
                        ('45', '45'), 
                        ('46', '46'),
                        ('47', '47'),
                        ('48', '48')]

SHOES_BRANDS_CHOICES = [('adidas', 'Adidas'),
                        ('nike', 'Nike')]
                        
class ShoesSearch(models.Model):
    sex = models.CharField(max_length=50, choices=SEX_CHOICES, default=SEX_CHOICES[0][0])
    brand = models.CharField(max_length=50, choices=SHOES_BRANDS_CHOICES, default=SHOES_BRANDS_CHOICES[0][0])
    size = models.CharField(max_length=50, choices=SHOES_SIZE_CHOICES, default=SHOES_SIZE_CHOICES[-3][0])

    def __str__(self):
        return self.brand

class ShoesItem(models.Model):
    brand = models.CharField(max_length=50)
    link = models.CharField(max_length=300)
    pic = models.CharField(max_length=300)
    disc_price = models.FloatField(max_length=10)
    org_price = models.FloatField(max_length=10)

    def __str__(self):
        return self.brand