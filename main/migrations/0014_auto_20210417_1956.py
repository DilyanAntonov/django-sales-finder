# Generated by Django 2.2.4 on 2021-04-17 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20210417_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoessearch',
            name='brand',
            field=models.CharField(choices=[('adidas', 'Adidas'), ('nike', 'Nike')], default='adidas', max_length=50),
        ),
        migrations.AlterField(
            model_name='shoessearch',
            name='size',
            field=models.CharField(choices=[('45', '45'), ('46', '46'), ('47', '47')], default='45', max_length=50),
        ),
    ]
