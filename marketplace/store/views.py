from django import views
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Product,Customer, Visited
from .category import Category
from django.contrib.auth.hashers import make_password, check_password
from django.views import  View
from django.contrib import messages
def index(request): #index page
    category = Category.get_all_categories()
    products = None
    catID = request.GET.get('category')
    if catID:
        products = Product.get_all_products_by_categoryid(catID)
        pass
    else:
        products = Product.get_all_products()
        pass
    data = {}
    data["products"] = products[::-1]
    data["category"] = category
    return render(request, 'index.html',data)
def detail(request): #detail page
    product = None
    proid = None
    proid = request.GET.get('prodid')
    product = Product.get_products_by_id(proid)
    if request.session['customer']:
        cid = request.session['customer']
        p = 0
        p =product[0].views + 1 #no. of views of a perticular product
        product.update(views = p)
        product[0].save()

        cus = Customer.objects.get(id=cid) #saving in visited table
        vis = Visited(email = cus.email, product =proid)
        vis.save()
        
    data = {}
    data["product"] = product
    data["id"]=product[0].productId
    return render(request,'details.html',data)
    pass

class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')
    def post(self,request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        customer = Customer(first_name=first_name,
                                last_name=last_name,
                                phone=phone,
                                email=email,
                                password=password)
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None
        error_message = self.validateCustomer(customer)
        if not error_message:
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('index')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)
    
    def validateCustomer(self,customer): # validating the data filled by customer in signup page
        error_message = None
        if (not customer.first_name):
            error_message = "First Name Required !!"
        elif len(customer.first_name) < 4:
            error_message = 'First Name must be 4 char long or more'
        elif not customer.last_name:
            error_message = 'Last Name Required'
        elif len(customer.last_name) < 4:
            error_message = 'Last Name must be 4 char long or more'
        elif not customer.phone:
            error_message = 'Phone Number required'
        elif len(customer.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len(customer.password) < 6:
            error_message = 'Password must be 6 char long'
        elif len(customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif customer.isExists():
            error_message = 'Email Address Already Registered..'
        return error_message
        

class Login(View):
    return_url = None
    def get(self , request):
        #Login.return_url = request.GET.get('return_url')
        return render(request , 'login.html')

    def post(self,request):  #login page
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                print('success')
                return redirect('dashboard')
            else:
                print('fail')
                error_message = 'Email or Password invalid !!'
                return render(request,'login.html',{'error':error_message})
        else:
            error_message = 'Email or Password invalid !!'
            return render(request,'login.html',{'error':error_message})
    pass

def logout(request):
    request.session.clear()
    return redirect('login')

def dashboard(request): #dashboard
    data = {}
    prod = None
    cid = request.session['customer']
    prod = Product.get_all_products_by_customerid(cid)
    category = Category.get_all_categories()
    
    visit_dict = {}
    
    for p in prod: #saving the list of users visited a perticular product
        lst = set()
        visited = Visited.objects.filter(product = p.productId)
        
        for v in visited:
            lst.add(v.email)
        if not len(lst) == 0:
            visit_dict[p.productId] = list(lst)
    data['prod']=prod[::-1]
    data['category'] = category
    data['visits'] = visit_dict
    print(request.method)
    if request.method == 'GET':
        
        return render(request,'dashboard.html',data)
    elif request.method == 'POST':
        postData = request.POST
        productId = postData.get('pid')
        category1 = postData.get('category')
        name = postData.get('pname')
        image = postData.get('pimage')
        stock = postData.get('stock')
        aprice = postData.get('aprice')
        sprice = postData.get('sprice')
        uid = postData.get('uid')
        
        prod = Product(   productId = productId,
        category  = Category.objects.get(id=category1),
        name      = name,
        image     = image,
        stock     = stock,
        price     = aprice,
        sprice    = sprice,
        uid       = Customer.objects.get(id=uid)
                        )
        if prod.isExists():
            error_message = 'Product already exists'
            data['error']= error_message,          
            return render(request,'dashboard.html',data)

        prod.save()
        return redirect('dashboard')
    pass
def delete(request):
    print('reached')
    proid = request.GET.get('prodid')
    print(proid)
    if proid:
        Product.objects.filter(productId = proid).delete()
    return redirect('dashboard')
def contact(request):
    messages.info(request, messages.INFO, 'Owner has benn notified')
    return redirect('index')
# def edit(request):
#     if request.method == 'POST':
#         proid = request.GET.get('prodid')
#         if proid:
#             category = Category.get_all_categories()
#             value = Product.get_products_by_id(proid)
#             data = {}
#             data['values'] = value[0]
#             data['category'] = category
#             return render(request,'edit.html',data)
#         postData = request.POST
#         productId = postData.get('pid')
#         category1 = postData.get('category')
#         name = postData.get('pname')
#         image = postData.get('pimage')
#         stock = postData.get('stock')
#         aprice = postData.get('aprice')
#         sprice = postData.get('sprice')
#         uid = postData.get('uid')
        
#         prod = Product(   productId = productId,
#         category  = Category.objects.get(id=category1),
#         name      = name,
#         image     = image,
#         stock     = stock,
#         price     = aprice,
#         sprice    = sprice,
#         uid       = Customer.objects.get(id=uid)
#                         )
#         #prod.update(sprice = sprice)
#         return redirect('dashboard')
                   
#     pass