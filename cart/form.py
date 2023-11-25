from django import forms

class login(forms.Form) :
    name = forms.CharField(required=False, label = 'account', widget= forms.TextInput(attrs={'placeholder':'name', 'required' : True}))
    password = forms.CharField(required=False, widget= forms.PasswordInput(attrs={'required' : True}))

class insertProduct(forms.Form) : # 新增商品
    name = forms.CharField(required=False, label = '商品名稱', widget= forms.TextInput(attrs={'placeholder':'name', 'required' : True}))
    price = forms.CharField(required=False, label = '商品價格', widget= forms.TextInput(attrs={'placeholder':'price', 'required' : True}))
    amount = forms.CharField(required=False, label = '商品數量', widget= forms.TextInput(attrs={'placeholder':'amount', 'required' : True}))

class delProduct(forms.Form) : # 刪除商品
    product = forms.CharField(required=False, label = '商品代號', widget= forms.TextInput(attrs={'placeholder':'product Id', 'required' : True}))

class updateProduct(forms.Form) : # 更新商品
    product = forms.CharField(required=False, label = '商品代號', widget= forms.TextInput(attrs={'placeholder':'product Id', 'required' : True}))
    name = forms.CharField(required=False, label = '商品名稱', widget= forms.TextInput(attrs={'placeholder':'name', 'required' : True}))
    price = forms.CharField(required=False, label = '商品價格', widget= forms.TextInput(attrs={'placeholder':'price', 'required' : True}))
    amount = forms.CharField(required=False, label = '商品數量', widget= forms.TextInput(attrs={'placeholder':'amount', 'required' : True}))

class insertCart(forms.Form) : # 新增至購物車
    product = forms.CharField(required=False, label = '商品代號', widget= forms.TextInput(attrs={'placeholder':'product Id', 'required' : True}))
    amount = forms.CharField(required=False, label = '商品數量', widget= forms.TextInput(attrs={'placeholder':'amount', 'required' : True}))

class delCart(forms.Form) : # 刪除商品
    cId = forms.CharField(required=False, label = '購物車代號', widget= forms.TextInput(attrs={'placeholder':'cart product Id', 'required' : True}))

class countCart(forms.Form) : # 刪除商品
    cId = forms.CharField(required=False, label = '購物車代號')

class deliverProduct(forms.Form) : # 刪除商品
    cId = forms.CharField(required=False, label = '購物車代號', widget= forms.TextInput(attrs={'placeholder':'cart product Id', 'required' : True}))
