from django.db import models

class User(models.Model):
    no = models.AutoField(primary_key=True)
    pwd = models.IntegerField(blank=True, null=True)  # 密碼
    title = models.CharField(max_length=10, blank=True, null=True)

class Product(models.Model):
    no = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 15, blank=True, null=True)  # 商品名稱
    price = models.IntegerField(blank=True, null=True) # 密碼
    stock = models.IntegerField(blank=True, null=True)   # 商品庫存量
    
class ShopCart(models.Model):
    no = models.AutoField(primary_key=True)
    user = models.IntegerField(blank=True, null=True) # 密碼
    product = models.IntegerField(blank=True, null=True) # 密碼
    amount = models.IntegerField(blank=True, null=True)  # 商品數量
    paid = models.BooleanField(default=True)  # 已付款
    delivered = models.BooleanField(default=False, blank=True, null=True)  # 已出貨
