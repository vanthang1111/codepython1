from django.shortcuts import render,redirect
from django.http import HttpResponse ,JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# Create your views here.
def detail(request):
    if request.user.is_authenticated:
        customer=request.user
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login="hidden"
        user_login="show"
    else:
        items=[]
        order={'get_cart_items':0,'get_cart_total':0 }
        cartItems = order['get_cart_items']
        user_not_login="show"
        user_login="hidden"
    id = request.GET.get('id','')
    products = Product.objects.filter(id=id)
    categories = Category.objects.filter(is_sub=False)
    context={'items':items,'order':order,'cartItems': cartItems,'user_not_login': user_not_login,'user_login': user_login,'categories': categories,'products': products}
    return render(request,'app/detail.html',context)
def register(request):
    form = CreateUserForm()
    
    if request.method =="POST":
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('login')

    context={'form':form}
    return render(request,'app/register.html',context)
def loginPage(request):
    user_not_login = "hidden"
    user_login = "hidden"  # Giả sử mặc định là ẩn, bạn có thể thay đổi nếu cần

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
            user_not_login = "hidden"
            user_login = "show"
        else:
            user_not_login = "show"
            user_login = "hidden"
            messages.info(request, 'Tài khoản hoặc mật khẩu sai')

    context = {'user_not_login': user_not_login, 'user_login': user_login}
    return render(request, 'app/login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('login')

def category(request):
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category', '')
    products = None  # Khởi tạo products là None

    if active_category:
        products = Product.objects.filter(category__slug=active_category)

    context = {'categories': categories, 'products': products, 'active_category': active_category}
    return render(request, 'app/category.html', context)


def search(request):
    if request.method =="POST":
        searched = request.POST["searched"]
        keys=Product.objects.filter(name__icontains = searched)
    if request.user.is_authenticated:
        customer=request.user
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login="hidden"
        user_login="show"
    else:
        items=[]
        order={'get_cart_items':0,'get_cart_total':0 }
        cartItems = order['get_cart_items']
        user_not_login="show"
        user_login="hidden"
    products=Product.objects.all()
    categories = Category.objects.filter(is_sub=False)

    
    return render(request,'app/search.html',{"searched" : searched,"keys" : keys,'products':products,'cartItems':cartItems,'user_not_login':user_not_login,'user_login':user_login,'categories':categories})
def home(request):
    
    if request.user.is_authenticated:
        customer=request.user
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login="hidden"
        user_login="show"
    else:
        items=[]
        order={'get_cart_items':0,'get_cart_total':0 }
        cartItems = order['get_cart_items']
        user_not_login="show"
        user_login="hidden"
    products=Product.objects.all()
    categories = Category.objects.filter(is_sub=False)
    context={'products':products,'cartItems':cartItems,'user_not_login':user_not_login,'user_login':user_login,'categories': categories}
    return render(request,'app/home.html',context)
def cart(request):
    if request.user.is_authenticated:
        customer=request.user
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login="hidden"
        user_login="show"
    else:
        items=[]
        order={'get_cart_items':0,'get_cart_total':0 }
        cartItems = order['get_cart_items']
        user_not_login="show"
        user_login="hidden"
    categories = Category.objects.filter(is_sub=False)
    context={'items':items,'order':order,'cartItems':cartItems,'user_not_login':user_not_login,'user_login':user_login,'categories': categories}
    return render(request,'app/cart.html',context)
def checkout(request):
    if request.user.is_authenticated:
        customer=request.user
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login="hidden"
        user_login="show"
    else:
        items=[]
        order={'get_cart_items':0,'get_cart_total':0 }
        cartItems = order['get_cart_items']
        user_not_login="show"
        user_login="hidden"
    categories = Category.objects.filter(is_sub=False)
    context={'items':items,'order':order,'cartItems':cartItems,'user_not_login':user_not_login,'user_login':user_login,'categories': categories}
    
    return render(request,'app/checkout.html',context)


def updateItem(request):
    data =json.loads(request.body)
    productId=data['productId']
    action=data['action']
    customer=request.user
    product=Product.objects.get(id=productId)
    order,created=Order.objects.get_or_create(customer=customer,complete=False)
    orderItem,created=Orderitem.objects.get_or_create(order=order,product=product)
    if action=='add':
        orderItem.quantity+=1
    elif action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()
    if orderItem.quantity<=0:
        orderItem.delete()
    
    return JsonResponse('added',safe=False)



