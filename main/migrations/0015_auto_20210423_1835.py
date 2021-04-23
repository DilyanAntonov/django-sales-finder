# Generated by Django 2.2.4 on 2021-04-23 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20210417_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clothessearch',
            name='clothes_type',
            field=models.CharField(choices=[('T-shirts', 'Тениски'), ('Hoodies', 'Суитшърти'), ('Tops', 'Блузи'), ('Jackets', 'Якета'), ('Pants', 'Долнища')], default='T-shirts', max_length=500),
        ),
        migrations.AlterField(
            model_name='clothessearch',
            name='size',
            field=models.CharField(choices=[('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('2XL', '2XL'), ('3XL', '3XL')], default='S', max_length=50),
        ),
        migrations.AlterField(
            model_name='shoessearch',
            name='size',
            field=models.CharField(choices=[('36', '36'), ('37', '37'), ('38', '38'), ('39', '39'), ('40', '40'), ('41', '41'), ('42', '42'), ('43', '43'), ('44', '44'), ('45', '45'), ('46', '46'), ('47', '47'), ('48', '48')], default='46', max_length=50),
        ),
    ]