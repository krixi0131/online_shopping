from django import forms

class login(forms.Form) :
    name = forms.CharField(required=False, label = 'account', widget= forms.TextInput(attrs={'placeholder':'name', 'required' : True}))
    password = forms.CharField(required=False, widget= forms.PasswordInput(attrs={'required' : True}))

class insertProduct(forms.Form) : # 新增商品至購物車
    name = forms.CharField(required=False, label = '商品名稱', widget= forms.TextInput(attrs={'placeholder':'name', 'required' : True}))
    price = forms.CharField(required=False, label = '商品價格', widget= forms.TextInput(attrs={'placeholder':'price', 'required' : True}))
    amount = forms.CharField(required=False, label = '商品數量', widget= forms.TextInput(attrs={'placeholder':'amount', 'required' : True}))

class delProduct(forms.Form) : # 刪除商品訂單
    product = forms.CharField(required=False, label = '商品代號', widget= forms.TextInput(attrs={'placeholder':'product Id', 'required' : True}))

class updateProduct(forms.Form) : # 更新商品本身的詳細訊息
    product = forms.CharField(required=False, label = '商品代號', widget= forms.TextInput(attrs={'placeholder':'product Id', 'required' : True}))
    name = forms.CharField(required=False, label = '商品名稱', widget= forms.TextInput(attrs={'placeholder':'name', 'required' : True}))
    price = forms.CharField(required=False, label = '商品價格', widget= forms.TextInput(attrs={'placeholder':'price', 'required' : True}))
    amount = forms.CharField(required=False, label = '商品數量', widget= forms.TextInput(attrs={'placeholder':'amount', 'required' : True}))


class insertCart(forms.Form) : # 新增至購物車
    product = forms.CharField(required=False, label = '商品代號', widget= forms.TextInput(attrs={'placeholder':'product Id', 'required' : True}))
    amount = forms.CharField(required=False, label = '商品數量', widget= forms.TextInput(attrs={'placeholder':'amount', 'required' : True}))

class delCart(forms.Form) : # 刪除商品
    cId = forms.CharField(required=False, label = '購物車代號', widget= forms.TextInput(attrs={'placeholder':'cart product Id', 'required' : True}))

class countCart(forms.Form) : # 接受客戶的訂單
    cId = forms.CharField(required=False, label = '購物車代號', widget= forms.TextInput(attrs={'placeholder':'cart product Id', 'required' : True}))

class confirmOrder(forms.Form) :  # 更新商品狀態至已確認訂單
    cId = forms.CharField(required=False, label = '購物車代號', widget= forms.TextInput(attrs={'placeholder':'cart product Id', 'required' : True}))

class deliverProduct(forms.Form) : # 更新商品狀態至寄送中
    cId = forms.CharField(required=False, label = '購物車代號', widget= forms.TextInput(attrs={'placeholder':'cart product Id', 'required' : True}))
class alreadySent(forms.Form) : #  # 更新商品狀態至已寄送
    cId = forms.CharField(required=False, label = '購物車代號', widget= forms.TextInput(attrs={'placeholder':'cart product Id', 'required' : True}))

class getCart(forms.Form) : # 取得商品資訊
    cId = forms.CharField(required=False, label = '購物車代號', widget= forms.TextInput(attrs={'placeholder':'cart product Id', 'required' : True}))