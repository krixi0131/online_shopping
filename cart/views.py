# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from .form import (
    login,
    insertProduct,
    delProduct,
    updateProduct,
    insertCart,
    delCart,
    countCart,
    deliverProduct,
    confirmOrder,
    alreadySent,
    getCart,
)
from .controller import loginController
import json
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


def loginPage(request):
    form_login = login(request.POST) # get the form
    error = []  # return error, and alert
    if request.method == "POST":
        if form_login.is_valid(): #
            cursor = connection.cursor() # # 連接資料庫
            cursor.execute("select `no`, `pwd`, `title`,`name` from cart_user;")
            all_users = cursor.fetchall()  # get all user in db

            name = request.POST["name"]
            pwd = request.POST["password"]

            correct = False  # 是否有找到帳密
            for i in range(len(all_users)): # check all user
                if str(all_users[i][3]) == name and str(all_users[i][1]) == pwd:  # 帳密正確
                    correct = True
                    request.session["user"] = all_users[i][0]  # record the session
                    request.session["title"] = all_users[i][2]
                    if all_users[i][2] == "customer":  # 若 title(角色) is customer
                        return redirect("/customerMain")  # 回傳顧客頁面
                    if all_users[i][2] == "seller":  # 若 title(角色) is seller
                        return redirect("/sellerMain")  # 回傳管理者頁面
                    if all_users[i][2] == "deliveryBoy":  # 若 title(角色) is seller
                        return redirect("/deliveryBoy")  # 回傳物流人員頁面
            if not correct:  # 帳密錯誤
                error.append("wrong account or password, login failed")

    context = {"error": error, "form_login": form_login} # 將錯誤訊息和表單傳到前端
    return render(request, "login.html", context) # 渲染 context 內容到 login.html


def deliveryBoy(request):  # 物流人員主頁面
    user = request.session.get("user") # get the user
    title = request.session.get("title") # get the title
    if title == "deliveryBoy":  # 是物流人員
        error = []
        cursor = connection.cursor() # # 連接資料庫
        Sent = alreadySent(request.POST) # 從前端取得已寄送的訂單
        if request.method == "POST":
            if "Sent" in request.POST:  # 物流收到商家的貨物並選擇寄送
                cId = request.POST["cId"]  # 訂單代號
                if 0 == cursor.execute(
                    "update cart_shopcart set `order_status` = '已寄送' where `no` = %s ", 
                    (cId,),# 更新訂單狀態為"已寄送"
                ):
                    error.append(
                        "can not deliver, as no this product Id"
                    )  # product is none
                else:
                    cursor.execute(
                        "select `product`, `amount`,`order_status` from cart_shopcart where `no` = %s",
                        (cId,),
                    )
                    cart_product = cursor.fetchone()
                    cursor.execute(
                        'update cart_shopcart set `order_status`="已寄送" where `no` = %s and `user` = %s',
                        (cId, user), # 更新訂單狀態為"已寄送"
                    ) 

        cursor.execute(
            "select * from cart_shopcart where `order_status` = '寄送中'"
        )  # select 出所有訂單狀態為"寄送中"的訂單
        deliver_orders = cursor.fetchall()  # 取得所有訂單狀態為"寄送中"的訂單

        context = {
            "error": error,
            "deliver_orders": deliver_orders,
            "user": user,
            "title": title,
            "alreadySent": Sent,
        }  # 將所有訂單狀態為"寄送中"的訂單傳到前端
        return render(
            request, "deliveryBoy.html", context
        )  # 渲染context內容到deliveryBoy.html
    else:
        return loginPage(request)  # 若不是物流人員，則返回登入頁面


def sellerMain(request):  # 商家主頁面
    user = request.session.get("user")
    title = request.session.get("title")
    if title == "seller":  # 是商家
        error = []
        cursor = connection.cursor() # 連接資料庫
        insert = insertProduct(request.POST) # 從前端取得新增商品的資訊
        delete = delProduct(request.POST) # 從前端取得刪除商品的資訊
        update = updateProduct(request.POST) # 從前端取得更新商品的資訊
        deliver = deliverProduct(request.POST) # 從前端取得更新訂單狀態為"寄送中"的資訊
        confirm = confirmOrder(request.POST) # 從前端取得更新訂單狀態為"處理中"的資訊
        if request.method == "POST": 
            if "insert" in request.POST:  # 新增商品
                name = request.POST["name"] # 商品名稱
                price = request.POST["price"] # 商品價格
                amount = request.POST["amount"] # 商品數量
                cursor.execute(
                    "insert into cart_product(`name`, `price`, `stock`) values(%s, %s, %s)",
                    (
                        name,
                        price,
                        amount,
                    ),# 將商品資訊新增到資料庫
                )
            if "del" in request.POST:  # 刪除商品
                product = request.POST["product"]
                cursor.execute("delete from cart_product where `no` = %s", (product,)) # 將商品資訊從資料庫刪除

            if "update" in request.POST:  # 更新商品本身的詳細訊息
                product = request.POST["product"]
                name = request.POST["name"]
                price = request.POST["price"]
                amount = request.POST["amount"]
                cursor.execute(
                    "update cart_product set `price` = %s, `stock` = %s, `name` = %s where `no` = %s",
                    (
                        price,
                        amount,
                        name,
                        product,
                    ), # 將商品資訊更新到資料庫
                )

            if "confirm" in request.POST:  # 確認訂單
                cId = request.POST["cId"] # 訂單代號
                if 0 == cursor.execute(
                    "update cart_shopcart set `order_status` = '處理中' where `no` = %s and `order_status`='未處理'",
                    (cId,),
                ):  # 更新訂單狀態為"處理中"
                    error.append(
                        "can not confirm, as no this product Id"
                    )  # product is none
                else:
                    cursor.execute(
                        "select `product`, `amount`,`order_status` from cart_shopcart where `no` = %s",
                        (cId,),
                    )  # select 出該訂單的商品代號、數量、訂單狀態
                    cart_product = cursor.fetchone() # 取得該訂單的商品代號、數量、訂單狀態
                    product = cart_product[0]  # the product Id of cart product
                    amount = cart_product[1]  # the amount of cart product
                    order_status = cart_product[2] # the order status of cart product
                    cursor.execute(
                        "select `stock` from cart_product where `no` = %s", (product,)
                    )  # select 出該商品的庫存
                    product_stock = cursor.fetchone()[0]  # 此商品的原始庫存
                    changed_num = product_stock - amount  # 更新後的庫存
                    cursor.execute(
                        "update cart_product set `stock` = %s where `no` = %s",
                        (
                            changed_num,
                            product,
                        ), # 將商品庫存更新到資料庫
                    )
                    cursor.execute(
                        'update cart_shopcart set `order_status`="處理中" where `no` = %s and `user` = %s',
                        (cId, user),
                    ) # 將訂單狀態更新到資料庫

            if "deliver" in request.POST:  # 寄送訂單
                cId = request.POST["cId"]
                if 0 == cursor.execute(
                    "update cart_shopcart set `order_status` = '寄送中' where `no` = %s and `order_status`='處理中'",
                    (cId,), # 更新訂單狀態為"寄送中"
                ):
                    error.append(
                        "can not deliver, as no this product Id"
                    )  # product is none
                else:
                    cursor.execute(
                        "select `product`, `amount`,`order_status` from cart_shopcart where `no` = %s",
                        (cId,),
                    )  # select 出該訂單的商品代號、數量、訂單狀態
                    cart_product = cursor.fetchone() # 取得該訂單的商品代號、數量、訂單狀態
                    product = cart_product[0]  # the product Id of cart product
                    amount = cart_product[1]  # the amount of cart product
                    order_status = cart_product[2]
                    cursor.execute(
                        "select `stock` from cart_product where `no` = %s", (product,)
                    )  # select 出該商品的庫存
                    product_stock = cursor.fetchone()[0]  # 此商品的原始庫存
                    cursor.execute(
                        'update cart_shopcart set `order_status`="寄送中" where `no` = %s and `user` = %s',
                        (cId, user), # 將訂單狀態更新成"寄送中"
                    ) # 將訂單狀態更新到資料庫

        cursor.execute("select * from cart_shopcart where `order_status` = '未處理'") # select 出所有訂單狀態為"未處理"的訂單
        sell_order_products = cursor.fetchall() # 取得所有訂單狀態為"未處理"的訂單

        cursor.execute("select * from cart_shopcart where `order_status` = '處理中'") # select 出所有訂單狀態為"處理中"的訂單
        sell_deliver_products = cursor.fetchall() # 取得所有訂單狀態為"處理中"的訂單

        cursor.execute("select * from cart_product") # select 出所有商品
        all_products = cursor.fetchall() # 取得所有商品

        cursor.execute(
            "select * from cart_shopcart where `paid` = 1 and `delivered` = 0;"
        )  # 該使用者還沒刪除的購物車商品
        cart_products = cursor.fetchall() # 取得該使用者還沒刪除的購物車商品
        context = {
            "error": error,
            "cart_products": cart_products,
            "deliverProduct": deliver,
            "user": user,
            "title": title,
            "insertProduct": insert,
            "delProduct": delete,
            "updateProduct": update,
            "all_products": all_products,
            "sell_order_products": sell_order_products,
            "sell_deliver_products": sell_deliver_products,
            "confirmOrder": confirm,
        }
        return render(request, "sellerMain.html", context) # 渲染context內容到sellerMain.html
    else:
        return loginPage(request) # 若不是商家，則返回登入頁面


@csrf_exempt
def customerMain(request):  # 客戶主頁面
    user = request.session.get("user") # get the user 
    title = request.session.get("title") # get the title
    body = request.body # get the body
    cursor = connection.cursor() # 連接資料庫
    try:
        body = json.loads(body.decode("utf-8")) # decode the body
        grade = body["grade"]  # get the grade
        cpid = body["id"] # get the id
        cursor.execute(
            "update cart_shopcart set `order_rating` =  %s where `no` = %s",
            (
                grade,
                cpid,
            ), # 將訂單評價更新到資料庫
        )

    except Exception as e:
        print(e)
        pass

    if title == "customer":  # 是客戶
        error = []  # return error, and alert
        insert = insertCart(request.POST) # 從前端取得新增商品的資訊
        delete = delCart(request.POST) # 從前端取得刪除商品的資訊
        count = countCart(request.POST) # 從前端取得接受訂單的資訊
        getC = getCart(request.POST) # 從前端取得客戶收到已送達訂單的資訊
        if request.method == "POST":  
            if "insert" in request.POST:  # 新增商品
                cursor.execute(
                    "select * from cart_product where `stock` > 0"
                )  # 還有庫存的商品
                all_products = cursor.fetchall() # 取得所有還有庫存的商品
                cursor.execute(
                    "select `product`, `amount` from cart_shopcart where `paid` = 1 and `delivered` = 0"
                )  # 找出已經被下單的商品
                reserved_products = cursor.fetchall() # 取得所有已經被下單的商品
                all_products = takeZero(
                    rmReversed(arrayOf(all_products), reserved_products)
                )  # 轉換tuple為list
                product = request.POST["product"]  # 商品代號
                amount = request.POST["amount"]  # 商品數量
                product_stock = findProduct(
                    all_products, product
                )  # 找出該商品的庫存
                if product_stock == None: # 沒有該商品
                    error.append("insert failed, as the cart_product Id is null")
                else:
                    if product_stock >= int(amount):  # stock的數量大於等於amount
                        cursor.execute(
                            "insert into cart_shopcart(`user`, `product`, `amount`, `paid`, `delivered`) values(%s, %s, %s, 0 , 0)",
                            (
                                user,
                                product,
                                amount,
                            ), # 將商品資訊新增到資料庫
                        )
                    else:
                        error.append("stock is not sufficient")
            if "delete" in request.POST:  # 刪除商品
                cId = request.POST["cId"]  # 商品代號
                if 0 == cursor.execute(
                    "delete from cart_shopcart where `no` = %s and `user` = %s",
                    (
                        cId,
                        user,
                    ), # 將商品資訊從資料庫刪除
                ):
                    error.append("can not delete, as no this id in your cart")
            if "count" in request.POST:  # 接受訂單
                cId = request.POST["cId"]  # 商品代號
                cursor.execute(
                    "select `user`,`product`, `amount`, `order_status` from cart_shopcart where `user` = %s",
                    (user,),
                )  # 找出該使用者的所有訂單
                cart_product = cursor.fetchall() # 取得該使用者的所有訂單
                order_status = cart_product[0][3] # 訂單狀態
                if len(cart_product) == 0: # 該使用者沒有訂單
                    error.append("can not update, as no product in your cart!")
                else:  # count successful
                    cursor.execute(
                        "update cart_shopcart set `paid` = 1  where `user` = %s ",
                        (user,),
                    )  # 將訂單狀態更新到資料庫
                    cursor.execute(
                        'update cart_shopcart set `order_status` = "未處理"  where `no` = %s and `user` = %s',
                        (cId, user), # 訂單狀態更新為"未處理"
                    )  # 將訂單狀態更新到資料庫
            if "getC" in request.POST: # 取得購物車
                cId = request.POST["cId"] # 訂單代號
                cursor.execute(
                    "select `user`,`product`, `amount`, `order_status` from cart_shopcart where `user` = %s",
                    (user,),
                ) # 找出該使用者的所有訂單
                cart_product = cursor.fetchall() # 取得該使用者的所有訂單
                order_status = cart_product[0][3] # 訂單狀態
                if len(cart_product) == 0: # 該使用者沒有訂單
                    error.append("can not update, as no product in your cart!")
                else:
                    if order_status == "已寄送":
                        cursor.execute(
                            'update cart_shopcart set `order_status` = "已送達"  where `no` = %s and `user` = %s',
                            (cId, user), # 訂單狀態更新為"已送達"
                        ) # 將訂單狀態更新到資料庫

        cursor.execute("select * from cart_shopcart where `user` = %s ", (user,)) # 找出該使用者的所有訂單
        order_products = cursor.fetchall() # 取得該使用者的所有訂單

        cursor.execute(
            "select * from cart_shopcart where `user` = %s and `paid` = 0", (user,)
        )  # select 出該使用者的購物車商品
        cart_products = cursor.fetchall() # 取得該使用者的購物車商品
        cursor.execute("select * from cart_product where `stock` > 0")  # select 出所有還有庫存的商品
        all_products = cursor.fetchall() # 取得所有還有庫存的商品
        cursor.execute(
            "select `product`, `amount` from cart_shopcart where `paid` = 1 and `delivered` = 0"
        )  # select 出已經被下單的商品
        reserved_products = cursor.fetchall() # 取得所有已經被下單的商品
        all_products = takeZero(
            rmReversed(arrayOf(all_products), reserved_products)
        )  # 轉換tuple為list
        context = {
            "count": count,
            "delete": delete,
            "error": error,
            "user": user,
            "title": title,
            "all_products": all_products,
            "insert": insert,
            "cart_products": cart_products,
            "order_products": order_products,
            "getCart": getC,
        }
        return render(request, "customerMain.html", context) # 渲染context內容到customerMain.html
    else:
        return loginPage(request) # 若不是客戶，則返回登入頁面


def Register(request):  # 註冊頁面
    if request.method == "POST":
        title = request.POST.get("title")  # get the title
        pwd = request.POST.get("pwd")  # get the password
        pwd = int(pwd) # turn the password to int
        name = request.POST.get("name") # get the name

        with connection.cursor() as cursor: # 連接資料庫
            cursor.execute(
                "INSERT INTO cart_user (pwd, title, name) VALUES (%s, %s, %s)", # 將註冊資訊新增到資料庫
                [pwd, title, name], 
            )
            cursor.execute("SELECT LAST_INSERT_ID()")  # select 出最後一筆資料的id
            result = cursor.fetchone() # 取得最後一筆資料的id
            if result is not None: # 註冊成功
                no = result[0]
            else:
                messages.error(request, "註冊失敗，請再試一次。")

        return redirect("/") # 回傳登入頁面

    return render(request, "register.html", context={"title": "註冊"}) # 渲染context內容到register.html

# 將tuple轉換為array
def arrayOf(tup):  
    total_array = []
    
    for each_tup in tup: # check all tuple
        each_array = []
        for each_tup_value in each_tup:
            each_array.append(each_tup_value) # add the value to each_array
        total_array.append(each_array) # add the array to total_array
    return total_array 

# 將已經被下單的商品從商品庫存中減去
def rmReversed(
    all_products, reserved_products #回傳減去已經被下單的商品後的商品
): 
    for product, amount in reserved_products:
        for i in range(len(all_products)):
            if all_products[i][0] == product: # 找到該商品
                all_products[i][3] -= amount  # 減去該商品的庫存
    return all_products

# 找出該商品的庫存
def findProduct(all_products, product):  #
    for each_products in all_products: # check all products
        if each_products[0] == int(product): # 找到該商品
            return each_products[3] # 回傳該商品的庫存
    return None

# 將庫存為0的商品從商品庫存中刪去
def takeZero(
    all_products,
):  
    new_all_products = []
    for each_product in all_products:
        if each_product[3] > 0: # 庫存大於0
            new_all_products.append(each_product)  # 將該商品加入new_all_products
    return new_all_products
