from .form import login, insertProduct, delProduct, updateProduct, insertCart, delCart, countCart, deliverProduct
from django.db import connection
from django.shortcuts import render, redirect

def loginController(request) :
    cursor = connection.cursor()
    cursor.execute("select `no`, `pwd`, `title`,`name` from cart_users;")
    all_users = cursor.fetchall()
    form_login = login(request.POST)
    if request.method == 'POST' :
        if form_login.is_valid():
            name = request.POST['name']
            pwd = request.POST['password']
            for i in range(len(all_users)):
                if (str(all_users[i][3]) == name and str(all_users[i][1]) == pwd) : # 帳密正確
                    request.session['user'] = all_users[i][0]
                    request.session['title'] = all_users[i][2]
                    if (all_users[i][2] == 'customer') :
                        return redirect('/customerMain')
                    if (all_users[i][2] == 'seller') :
                        return redirect('/sellerMain')
    return None
