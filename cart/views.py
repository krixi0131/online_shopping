# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from .form import login, insertProduct, delProduct, updateProduct, insertCart, delCart, countCart, deliverProduct
#from .controller import loginController
import json


def loginPage(request) :
    form_login = login(request.POST)
    error = [] # return error, and alert
    if request.method == 'POST' :
        if form_login.is_valid():
            cursor = connection.cursor()
            cursor.execute("select `no`, `pwd`, `title` from cart_user;")
            all_users = cursor.fetchall() # get all user in db
            name = request.POST['name']
            pwd = request.POST['password']
            
            correct = False # whether login correctly
            #print(all_users[i])
            for i in range(len(all_users)):
                if (str(all_users[i][0]) == name and str(all_users[i][1]) == pwd) : # 帳密正確
                    correct = True
                    #print("cor")
                    request.session['user'] = all_users[i][0] # record the session
                    request.session['title'] = all_users[i][2]
                    if (all_users[i][2] == 'customer') : # title is customer
                        return redirect('/customerMain') # return to customer page
                    if (all_users[i][2] == 'seller') : # title is seller
                        return redirect('/sellerMain') # return to seller page
            if not correct : # wrong account or pwd 
                error.append('wrong account or pwd, login failed')
    context = {"error" : error, "form_login" : form_login}
    return render(request, 'login.html', context); 

def customerMain(request) : # 顧客主頁面
    user = request.session.get('user')
    title = request.session.get('title')
    error = [] # return error, and alert
    if (user and title == 'customer') : # 是顧客
        cursor = connection.cursor()
        insert = insertCart(request.POST)
        delete = delCart(request.POST)
        count = countCart(request.POST)
        
        if request.method == 'POST' : # POST
            if 'insert' in request.POST : # 新增商品
               cursor.execute("select * from cart_product where `stock` > 0") # 還有庫存的商品
               all_products = cursor.fetchall()
               cursor.execute("select `product`, `amount` from cart_shopcart where `paid` = 1 and `delivered` = 0") # find the reserved products
               reserved_products = cursor.fetchall()
               all_products = takeZero(rmReversed(arrayOf(all_products), reserved_products)) # turn tuple to list
               product = request.POST['product'] # 商品代號
               amount = request.POST['amount'] # 要多少件商品
               product_stock = findProduct(all_products, product) # find the right stock of product
               if (product_stock == None) :
                   error.append('insert failed, as the cart_product Id is null')
               else :
                   if (product_stock >= int(amount)) : # requirement not over the stock
                       cursor.execute("insert into cart_shopcart(`user`, `product`, `amount`, `paid`, `delivered`) values(%s, %s, %s, 0 , 0)", (user, product, amount,))
                   else :
                       error.append('stock is not sufficient')
            if 'delete' in request.POST : # 新增商品
               cId = request.POST['cId'] # 商品代號
               if (0 == cursor.execute('delete from cart_shopcart where `no` = %s and `user` = %s', (cId, user,))) : 
                   error.append('can not delete, as no this id in your cart')
            if 'count' in request.POST : # 新增商品
               #cId = request.POST['cId'] # 商品代號
               cursor.execute('select `product`, `amount` from cart_shopcart where `user` = %s and `delivered` = 0 and `paid` = 0', (user,)) # cart product is in cart and be counted
               cart_product = cursor.fetchall()
               if (len(cart_product) == 0) :
                   error.append('can not update, as no product in your cart')
               else : # count successful
                   cursor.execute('update cart_shopcart set `paid` = 1 where `user` = %s and `delivered` = 0', (user,)) # set cart product is paid
        cursor.execute("select * from cart_shopcart where `user` = %s and `paid` = 0", (user,)) # 該使用者還沒刪除的購物車商品
        cart_products = cursor.fetchall()
        cursor.execute("select * from cart_product where `stock` > 0") # 還有庫存的商品
        all_products = cursor.fetchall()
        cursor.execute("select `product`, `amount` from cart_shopcart where `paid` = 1 and `delivered` = 0") # find the reserved products
        reserved_products = cursor.fetchall()
        all_products = takeZero(rmReversed(arrayOf(all_products), reserved_products)) # turn tuple to list
        #print(all_products)
        print(cart_products)
        context = {'count' : count, 'delete' : delete, 'error' : error, 'user' : user, 'title' : title, 'all_products' : all_products, 'insert' : insert, 'cart_products' : cart_products}
        return render(request, 'customerMain.html', context) 
    else :
        return loginPage(request)

def sellerMain(request) : # 管理者主頁面
    user = request.session.get('user')
    title = request.session.get('title')
    if (user and title == 'seller') : # 是管理者
        error = []
        cursor = connection.cursor()
        insert = insertProduct(request.POST)
        delete = delProduct(request.POST)
        update = updateProduct(request.POST)
        deliver = deliverProduct(request.POST)
        if request.method == 'POST' :
            if 'insert' in request.POST : # 新增商品
                name = request.POST['name']
                price = request.POST['price']
                amount = request.POST['amount']
                cursor.execute("insert into cart_product(`name`, `price`, `stock`) values(%s, %s, %s)", (name, price, amount,))
            if 'del' in request.POST : # 刪除商品
                product = request.POST['product']
                cursor.execute("delete from cart_product where `no` = %s", (product,))
            if 'update' in request.POST : # 刪除商品
                product = request.POST['product']
                name = request.POST['name']
                price = request.POST['price']
                amount = request.POST['amount']
                cursor.execute("update cart_product set `price` = %s, `stock` = %s, `name` = %s where `no` = %s", (price, amount, name, product,))
            if 'deliver' in request.POST : # 刪除商品
                cId = request.POST['cId']
                if 0 == cursor.execute("update cart_shopcart set `delivered` = 1 where `no` = %s and `delivered` = 0", (cId,)) : # update cart product to is delivered where it is not deliver
                    error.append('can not deliver, as no this product Id') # product is none
                else :
                   cursor.execute('select `product`, `amount` from cart_shopcart where `no` = %s', (cId,)) # find the stock
                   cart_product = cursor.fetchone()
                   product = cart_product[0] # the product Id of cart product
                   amount = cart_product[1] # the amount of cart product
                   cursor.execute('select `stock` from cart_product where `no` = %s', (product,)) # find the stock
                   product_stock = cursor.fetchone()[0] # this product original stock
                   changed_num = product_stock - amount # original stock - are buy
                   cursor.execute('update cart_product set `stock` = %s where `no` = %s', (changed_num, product,))
        cursor.execute("select * from cart_product")
        all_products = cursor.fetchall()
        cursor.execute("select * from cart_shopcart where `paid` = 1 and `delivered` = 0;") # the cart product is paid and not delivered yet
        cart_products = cursor.fetchall()
        context = {'error' : error, 'cart_products' : cart_products, 'deliverProduct' : deliver, 'user' : user, 'title' : title, 'insertProduct' : insert, 'delProduct' : delete, 'updateProduct' : update, "all_products" : all_products}
        return render(request, 'sellerMain.html', context) 
    else :
        return loginPage(request)

def arrayOf(tup) : # turn tuple to array
    total_array = []
    # two layer tuple
    for each_tup in tup :
        each_array = []
        for each_tup_value in each_tup :
            each_array.append(each_tup_value)
        total_array.append(each_array)
    return total_array

def rmReversed(all_products, reserved_products) : # return the minus reserved all_products
    for product, amount in reserved_products :
        for i in range(len(all_products)) :
            if (all_products[i][0] == product) :
                all_products[i][3] -= amount # minus the num of reserved
    return all_products

def findProduct(all_products, product) : # return the value of the product's stock
    for each_products in all_products :
        if (each_products[0] == int(product)) :
            return each_products[3]
    return None

def takeZero(all_products) : # take out the product which stock is <= where is minus the reserved
    new_all_products = []
    for each_product in all_products :
        if (each_product[3] > 0) : # stock is > 0
            new_all_products.append(each_product) # add product
    return new_all_products

