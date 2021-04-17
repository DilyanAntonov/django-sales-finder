# Generated by Django 2.2.4 on 2021-04-17 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20210409_1731'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClothesSearch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sex', models.CharField(choices=[('Man', 'МЪЖЕ'), ('Women', 'ЖЕНИ')], default='S', max_length=50)),
                ('size', models.CharField(choices=[('S', 's'), ('M', 'm'), ('L', 'l'), ('XL', 'xl'), ('2XL', '2xl'), ('3XL', '3xl')], default='S', max_length=50)),
                ('brand', models.CharField(choices=[('superdry', 'Superdry'), ('diesel', 'Diesel'), ('adidas', 'Adidas'), ('napapijri', 'Napapijri')], default='superdry', max_length=50)),
                ('clothes_type', models.CharField(choices=[('T-shirts', 'Тениски'), ('Hoodies', 'Суитшърти'), ('Tops', 'Блузи'), ('Jackets', 'Якета')], default='T-shirts', max_length=500)),
            ],
        ),
        migrations.RenameModel(
            old_name='Item',
            new_name='ClothesItem',
        ),
        migrations.DeleteModel(
            name='Search',
        ),
    ]
