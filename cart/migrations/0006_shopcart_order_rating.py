# Generated by Django 4.2.7 on 2024-01-06 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_alter_shopcart_product_alter_shopcart_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopcart',
            name='order_rating',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]