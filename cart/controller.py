from .form import (
    login,
    insertProduct,
    delProduct,
    updateProduct,
    insertCart,
    delCart,
    countCart,
    deliverProduct,
)
from django.db import connection
from django.shortcuts import render, redirect

# 顯示登入頁面
def loginController(request):
    cursor = connection.cursor() # 連接資料庫
    cursor.execute("select `no`, `pwd`, `title`,`name` from cart_users;") # select 所有使用者資料
    all_users = cursor.fetchall() # 取得所有使用者資料
    form_login = login(request.POST) # 建立登入表單
    if request.method == "POST":
        if form_login.is_valid():
            name = request.POST["name"]
            pwd = request.POST["password"]
            for i in range(len(all_users)): # 比對帳密
                if str(all_users[i][3]) == name and str(all_users[i][1]) == pwd:  # 帳密正確
                    request.session["user"] = all_users[i][0] # 儲存使用者編號
                    request.session["title"] = all_users[i][2] # 儲存使用者身分
                    if all_users[i][2] == "customer":
                        return redirect("/customerMain") # 客戶頁面
                    if all_users[i][2] == "seller":
                        return redirect("/sellerMain") # 商家頁面
                    if all_users[i][2] == "deliveryBoy":
                        return redirect("/deliveryBoy") # 物流人員頁面
    return None # 帳密錯誤
