from django.db import models
from django.conf import settings
class User(models.Model):
    no = models.AutoField(primary_key=True)
    pwd = models.CharField(max_length=20,blank=True,null=True)  # 密碼
    title = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=20, blank=True, null=True)

class Product(models.Model):
    no = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 15, blank=True, null=True)  # 商品名稱
    price = models.IntegerField(blank=True, null=True) # 密碼
    stock = models.IntegerField(blank=True, null=True)   # 商品庫存量

class shopCart(models.Model):
    ORDER_STATUS_CHOICES = [
        ('未處理', '未處理'),
        ('處理中', '處理中'),
        ('寄送中', '寄送中'),
        ('已寄送', '已寄送'),
        ('已送達', '已送達'),
    ]
    no = models.AutoField(primary_key=True)
    user = models.IntegerField(blank=True, null=True)
    product = models.IntegerField(blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)  # 商品數量  
    paid = models.BooleanField(default=True)  # 已付款
    delivered = models.BooleanField(default=False, blank=True, null=True)  # 已被購買
    order_status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES, default='未處理')  # 訂單狀態
    order_rating = models.IntegerField(blank=True, null=True) # 訂單評價5分制，評價滿意度(1-5顆星)

