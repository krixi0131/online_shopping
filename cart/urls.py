from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.loginPage), # 登入頁面
    path("customerMain", views.customerMain), # 顧客頁面
    path("sellerMain", views.sellerMain), # 商家頁面
    path("register/", views.Register), # 註冊頁面
    path("deliveryBoy", views.deliveryBoy), # 物流人員頁面
]
