from django.shortcuts import render,redirect
from AdminApp.models import Category,ClothItems

from .models import User,Wishlist,Cart
from django.http import JsonResponse,HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def user_login(request):
    message = 'valid'
    if request.method == 'POST':
        data = request.POST
        name = data.get("username")
        password = data.get("password")
        is_valid_user= User.objects.filter(username = name, password = password)
        if is_valid_user:
            request.session['username'] = name
            return redirect('/home')
        else:
            message = 'invalid'
    return render(request,'loginpage.html',{"msg":message})

def user_signup(request):
    if request.method == 'POST':
        data = request.POST
        name = data.get("name")
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        User.objects.create(name = name,username = username,email = email,password = password)
        print("success")

    return render(request,'user-signup.html')

def user_logout(request):
    try:
     del request.session['username']
    except KeyError :
        pass
    return redirect('/userlogin')


def home(request):
    if 'username' in request.session:
        category = Category.objects.all()
        name = request.session['username']
        user = User.objects.get(username = name)
        wishlists = Wishlist.objects.filter(user=user.user_id)
        return render(request, 'index.html',{"user":user,"category":category,"wishlist":wishlists})
    else:
        return redirect('/userlogin')


def show_products(request,id):
    if 'username' in request.session:
        name = request.session['username']
        user = User.objects.get(username=name)
        category = Category.objects.get(category_id = id)
        clothitems = ClothItems.objects.filter(category = id)
        if request.method == 'POST':
            cloth_id = request.POST.get('item_id')
            clothitem = ClothItems.objects.get(item_id = cloth_id)
            try:
             wishlists = Wishlist.objects.get(user=user.user_id , cloth_item = clothitem)
             if wishlists:
                 pass
             else:
                 Wishlist.objects.create(user=user, cloth_item=clothitem)
            except Wishlist.DoesNotExist:
                Wishlist.objects.create(user=user, cloth_item=clothitem)
                print("created")


        wishlists = Wishlist.objects.filter(user = user.user_id)
        return render(request,'topwears.html',{
                       "user":user,
                       "clothitems":clothitems,
                       "category":category,
                       "wishlist":wishlists
        })
    else:
        return redirect('/userlogin')

def produt_description(request,category,id):
    if 'username' in request.session:
        name = request.session['username']
        user = User.objects.get(username=name)
        category = Category.objects.get(category_name = category)
        clothitem = ClothItems.objects.get(item_id = id)
        wishlists = Wishlist.objects.filter(user=user.user_id)
    return render(request,'p_desc.html',{"user":user,"clothitem":clothitem,"category":category,"wishlist":wishlists})


def deletefromwishlist(request,id):
    item = Wishlist.objects.get(wishlist_id = id)
    item.delete()
    return none


def show_order(request,category, id1):
    try:
        category = Category.objects.get(category_name=category)
        clothitem = ClothItems.objects.get(item_id=id1)
    except ClothItems.DoesNotExist:
        return HttpResponseNotFound("Cloth item not found")

    return render(request, 'user-order.html', {"clothitem": clothitem})


def show_cart(request):
    user_name = request.session['username']
    user = User.objects.get(username = user_name)
    cart_items = Cart.objects.filter(user=user.user_id)

    return render(request,'user-cart.html',{'cart_items':cart_items})

def show_user_profile(request):
    return render(request,'user-profile.html')


def add_to_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        user = request.session['username']
        if user:
            user1 = User.objects.get(username = user)
            cloth_item = ClothItems.objects.get(item_id = item_id)

            try:
                in_cart = Cart.objects.get(cloth_item = item_id,user = user1)

                if in_cart:
                    return JsonResponse({'message': 'item already in cart'})
                else:
                    new_cart_item = Cart.objects.create(user= user1, cloth_item = cloth_item)
            except Cart.DoesNotExist:
                new_cart_item = Cart.objects.create(user=user1, cloth_item=cloth_item)
            return JsonResponse({'message':'success'})
        else:
            return JsonResponse({'message':'user not authenticated'},status=401)
    return JsonResponse({'message': 'Failed'}, status=400)
