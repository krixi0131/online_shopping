# Generated by Django 4.2.7 on 2024-01-06 05:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_shopcarts'),
    ]

    operations = [
        migrations.DeleteModel(
            name='shopCart',
        ),
    ]