from django.shortcuts import render, redirect, HttpResponse
from .models import Category, ClothItems, ItemImages, ClothSpecification, Admin
from django.contrib.auth import login, authenticate
from .form import UserForm
from django.contrib.auth.models import User


# Create your views here.

# def admin_login(request):
#     message = 'valid'
#     if request.method == 'POST':
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         try:
#             is_valid = Admin.objects.get(admin_username=username, admin_password=password)
#             if is_valid:
#                 request.session['username'] = username
#                 return redirect('/')
#             else:
#                 message = 'invalid'
#         except Admin.DoesNotExist:
#             message = 'invalid'
#
#     return render(request, 'admin-login.html', {"msg": message})

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = User()
            user.username = request.POST.get('username')
            user.set_password(request.POST.get('password'))
            user.email = request.POST.get('email')
            user.save()
            message = 'account created'
            return render(request, 'admin-signup.html', {'form': form,'msg':message})
    else:
        form = UserForm()
    return render(request, 'admin-signup.html', {'form': form})




# def admin_signup(request):
#     message = "none"
#     if request.method == 'POST':
#         username = request.POST.get("admin_username")
#         password = request.POST.get("admin_password")
#         mail = request.POST.get("admin_email")
#
#         Admin.objects.create(admin_username=username, admin_password=password, admin_mail=mail)
#         message = "account created successfully"
#
#     return render(request, 'admin-signup.html', {"msg": message})


# def admin_logout(request):
#     del request.session['username']
#     return redirect('/adminLogin')


def home(request):
    if 'username' in request.session:
        name = request.session['username']
        user_data = Admin.objects.filter(admin_username=name)
        return render(request, 'dashboard.html', {'user_data': user_data})
    else:
        return redirect('/adminLogin')


def add_category(request):
    if request.method == 'POST':
        category_title = request.POST.get('categoryName')
        category_img = request.FILES.get('categoryImg')

        cat_obj = Category()
        cat_obj.category_name = category_title
        cat_obj.category_img = category_img
        cat_obj.save()

    return render(request, 'add-category.html')


def delete_category(request, id):
    data = Category.objects.get(category_id=id)
    data.delete()
    return redirect('/category')


def update_category(request, id):
    category = Category.objects.get(category_id=id)
    if request.method == 'POST':
        category.category_name = request.POST.get('categoryName')
        category.category_img = request.FILES.get('categoryImg')
        category.save()
        return redirect('/category')
    return render(request, 'add-category.html', {'data': category})


def view_category(request):
    categories = Category.objects.all()
    return render(request, 'view-category.html', {"data": categories})


def add_product(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        product_name = request.POST.get('itemName')
        product_desc = request.POST.get('itemDesc')
        product_cat_id = request.POST.get('itemCat')
        product_cat = Category.objects.get(category_id=product_cat_id)
        product_price = request.POST.get('itemPrice')
        product_stock = request.POST.get('stock')

        clothItem = ClothItems.objects.create(
            category=product_cat,
            item_name=product_name,
            description=product_desc,
            price=product_price,
            stock=product_stock,

        )

        for size in request.POST.getlist('size'):
            ClothSpecification.objects.create(cloth_item=clothItem, item_size=size)

        for img in request.FILES.getlist('itemImg'):
            ItemImages.objects.create(cloth_item=clothItem, image_url=img)

    return render(request, 'add-product.html', {'data': categories})


def view_product(request):
    products = ClothItems.objects.all()
    category = Category.objects.all()
    return render(request, 'view-products.html', {'products': products,"category":category})

def view_products_categorize(request,id):
    products = ClothItems.objects.filter(category = id)
    category = Category.objects.all()
    return render(request,'view-products.html',{'products':products,"category":category})


def order_list(request):
    return render(request, 'order-list.html')


def order_details(request):
    return render(request, 'order-details.html')


def transaction_list(request):
    return render(request, 'transaction-list.html')


def transaction_details(request):
    return render(request, 'transaction-details.html')


def profile(request):
    return render(request, 'profile-setting.html')
