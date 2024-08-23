from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from AdminApp.models import Category, ClothItems, Size, District, State, ItemImages

from .models import User, Wishlist, Cart, Address, Order, OrderItems, OTP, PaymentModel
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest
import random
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.core.paginator import Paginator
import razorpay
from project import settings
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def otp_page(request):
    if request.method == 'POST':
        mail = request.POST.get('email')
        request.session['mail'] = mail
        if not OTP.objects.filter(mail=mail).exists():
            otp = OTP()
            otp.generate_otp(mail)
            print(timezone.now())
            print(timedelta(minutes=10))
            send_mail(
                'Your OTP for Signup',
                f'Your OTP is {otp.otp}',
                'soorajsundaran66@gmail.com',
                [mail],
                fail_silently=False,
            )

            return redirect('/newuser/verify-otp')
        else:
            pass
    return render(request, 'otp-page.html')


def verify_otp(request):
    if request.method == 'POST':
        mail = request.session['mail']
        otp = OTP.objects.get(mail=mail)
        otp_received = request.POST.get('otp-received')
        otp.verify_otp(otp_received)
        otp.delete()
        return redirect('/usersignup')
    return render(request, 'verify-otp.html')


def user_login(request):
    message = 'valid'
    if request.method == 'POST':
        data = request.POST
        name = data.get("username")
        password = data.get("password")
        is_valid_user = User.objects.filter(username=name, password=password)
        if is_valid_user:
            request.session['username'] = name
            return redirect('/home')
        else:
            message = 'invalid'
    return render(request, 'loginpage.html', {"msg": message})


def user_signup(request):
    if request.method == 'POST':
        data = request.POST
        firstname = data.get("firstname")
        secondname = data.get("secondname")
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        User.objects.create(firstname=firstname, secondname=secondname, username=username, email=email,
                            password=password)
        print("success")

    return render(request, 'user-signup.html')


def user_logout(request):
    try:
        del request.session['username']
    except KeyError:
        pass
    return redirect('/userlogin')


def home(request):
    if 'username' in request.session:
        username = request.session['username']
        category = Category.objects.all()
        user = User.objects.get(username=username)
        clothitems = list(ClothItems.objects.all())
        random.shuffle(clothitems)
        clothitems = clothitems[:4]
        wishlists = Wishlist.objects.filter(user=user.user_id)
        return render(request, 'index.html',
                      {"user": user, "category": category, "wishlist": wishlists, "clothitems": clothitems})
    else:
        return redirect('/userlogin')


def show_products(request, id):
    if 'username' in request.session:

        page = 1
        if request.GET:
            page = request.GET.get('page', 1)
        name = request.session['username']
        user = User.objects.get(username=name)
        category = Category.objects.get(category_id=id)
        wishlists = Wishlist.objects.filter(user=user.user_id)
        clothitems = ClothItems.objects.filter(category=id)
        product_paginator = Paginator(clothitems, 2)
        clothitems = product_paginator.get_page(page)

        sizes = Size.objects.all()
        if request.method == 'POST':
            size_id = request.POST.get('size_id')
            price = request.POST.get('price')
            category_id = request.POST.get('category_id')
            if size_id != 0:
                try:
                    size = Size.objects.get(size_id=size_id)
                    clothitems = ClothItems.objects.filter(category=category_id, clothspec__size=size)
                except Size.DoesNotExist:
                    clothitems = ClothItems.objects.filter(category=category_id)
            else:
                clothitems = ClothItems.objects.filter(category=id)

            if price == 'low':
                clothitems = clothitems.order_by('price')
            elif price == 'high':
                clothitems = clothitems.order_by('-price')

            product_paginator = Paginator(clothitems, 2)
            clothitems = product_paginator.get_page(page)

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                clothitems_html = render_to_string('clothitems.html', {'clothitems': clothitems})
                return JsonResponse({'clothitems_html': clothitems_html})

        return render(request, 'topwears.html', {
            "user": user,
            "clothitems": clothitems,
            "category": category,
            "wishlist": wishlists,
            "sizes": sizes
        })
    else:
        return redirect('/userlogin')


def add_to_wishlist(request, catid, itmid):
    if 'username' in request.session:
        username = request.session['username']
        user = User.objects.get(username=username)
        if request.method == 'POST':
            category = Category.objects.get(category_id=catid)
            clothitem = ClothItems.objects.get(item_id=itmid)
            try:
                in_wishlist = Wishlist.objects.get(user=user, cloth_item=clothitem)
                if in_wishlist:
                    print("already")
                    return JsonResponse({'message': 'item already in wishlist'})
                else:
                    Wishlist.objects.create(user=user, cloth_item=clothitem)
            except Wishlist.DoesNotExist:
                Wishlist.objects.create(user=user, cloth_item=clothitem)

            wishlist_items = Wishlist.objects.filter(user=user)
            wishlist_html = render_to_string('wishlist_items.html', {'wishlist': wishlist_items})
            print("added")
            return JsonResponse({'message': 'success', 'wishlist_html': wishlist_html})
        else:
            print("failed")
            return JsonResponse({'message': 'Failed'}, status=400)
    else:
        return redirect('/home')


def produt_description(request, category, id):
    if 'username' in request.session:
        name = request.session['username']
        user = User.objects.get(username=name)
        category = Category.objects.get(category_name=category)
        clothitem = ClothItems.objects.get(item_id=id)
        wishlists = Wishlist.objects.filter(user=user.user_id)
        similaritems = list(ClothItems.objects.filter(category=category).exclude(item_id=id))  #for shuffling item
        random.shuffle(similaritems)
        similaritems = similaritems[:5]
        # if request.method == "POST":
        #     selected_size = request.POST.get('size_id')
        #     if selected_size is None:
        #         return render(request, 'p_desc.html', {
        #             'clothitem': clothitem,
        #             "category": category,
        #             'error_message': 'Please select a size.'
        #         })
        #     else:
        #         size = Size.objects.get(size_id=selected_size)
        #         return render(request, 'user-order.html', {
        #             'user':user,
        #             'clothitem': clothitem,
        #             'size': size,
        #             'quantity_range': range(1, 6)
        #         })
        return render(request, 'p_desc.html',
                      {"user": user, "clothitem": clothitem, "category": category, "wishlist": wishlists,
                       "similaritems": similaritems})
    else:
        return redirect('/userlogin')


def deletefromwishlist(request, id):
    if 'username' in request.session:
        username = request.session['username']
        user = User.objects.get(username=username)
        if request.method == 'POST':
            try:
                wishlist_item = Wishlist.objects.get(user=user.user_id, cloth_item=id)
                wishlist_item.delete()
            except Wishlist.DoesNotExist:
                return HttpResponseNotFound("not found")
    return redirect(request.META.get('HTTP_REFERER', '/'))


def deletefromcart(request, id):
    if 'username' in request.session:
        username = request.session['username']
        user = User.objects.get(username=username)
        if request.method == 'POST':
            try:
                cart_item = Cart.objects.get(user=user.user_id, cloth_item=id)
                cart_item.delete()
            except ClothItems.DoesNotExist:
                return HttpResponseNotFound("not found")
    return redirect('/cart')


# def show_order(request, category, id1):
#     if request.method == 'POST':
#         username = request.session.get('username')
#         if username:
#             try:
#                 user = User.objects.get(username=username)
#                 wishlists = Wishlist.objects.filter(user=user.user_id)
#                 size_id = request.POST.get("size_id")
#
#                 if not size_id:  # Check if size_id is provided
#                     return JsonResponse({"message": "Please select a size."})
#
#                 categoryname = request.POST.get("category_name")
#                 clothitem_id = request.POST.get("item_id")
#                 clothitem = ClothItems.objects.get(item_id=clothitem_id)
#                 category = Category.objects.get(category_name=categoryname)
#                 size = Size.objects.get(size_id=size_id)
#
#                 return render(request, 'user-order.html', {
#                     "clothitem": clothitem,
#                     "category": category,
#                     "size": size,
#                     "wishlist": wishlists
#                 })
#             except (User.DoesNotExist, ClothItems.DoesNotExist, Category.DoesNotExist, Size.DoesNotExist) as e:
#                 return JsonResponse({"message": "An error occurred while processing the order"})
#         else:
#             return JsonResponse({"message": "User not authenticated"})
#     else:
#         url = reverse('product_description', args=[category, id1])
#         return redirect(url)

#
# def buy_now(request, item_id):
#     cloth_item = ClothItems.objects.get(item_id=item_id)
#     if request.method == "POST":
#         selected_size = request.POST.get('size_id')
#         print(selected_size)
#         if not selected_size :
#             return render(request, 'p_desc.html', {
#                 'clothitem': cloth_item,
#                 'error_message': 'Please select a size.'
#             })
#         else:
#             size = Size.objects.get(size_id = selected_size)
#             return render(request, 'user-order.html', {
#                 'clothitem': cloth_item,
#                 'size': size,
#                 'quantity_range': range(1, 6)
#             })
#
#     return render(request, 'p_desc.html', {'clothitem': cloth_item})


def show_order(request):
    if 'username' in request.session:
        name = request.session['username']
        user = User.objects.get(username=name)
        cart_items = Cart.objects.filter(user=user.user_id)
        wishlists = Wishlist.objects.filter(user=user.user_id)
        if 'clothitem' in request.session:
            clothitem_id = request.session.get('clothitem')
            clothitem = ClothItems.objects.get(item_id=clothitem_id)
        if 'size' in request.session and request.session['size'] is not None:
            size_id = request.session.get('size')
            size = Size.objects.get(size_id=size_id)
        if request.method == "POST" and 'buy-now-identity' in request.POST:
            categoryname = request.POST.get("categoryname")
            item_id = request.POST.get("item_id")
            category = Category.objects.get(category_name=categoryname)
            clothitem = ClothItems.objects.get(item_id=item_id)
            request.session['clothitem'] = clothitem.item_id
            selected_size = request.POST.get('size_id')
            request.session['size'] = selected_size
            in_stock = request.POST.get('in_stock')
            if in_stock is not None:
                if selected_size is None:
                    messages.error(request, 'Please select size')
                    return redirect(request.META.get('HTTP_REFERER'))
                else:
                    size = Size.objects.get(size_id=selected_size)
                    return render(request, 'user-order.html', {
                        'user': user,
                        'clothitem': clothitem,
                        'size': size,
                        'quantity_range': range(1, 6)
                    })

        elif request.method == 'POST' and 'cart-identity' in request.POST:
            total_items = int(request.POST.get('total_items', 0))
            items_data = []

            for i in range(1, total_items + 1):
                item_id = request.POST.get(f'item_id_{i}')
                quantity = request.POST.get(f'quantity_{i}')
                size_id = request.POST.get(f'size_{i}')

                if item_id and size_id:
                    item = ClothItems.objects.get(item_id=item_id)
                    size = Size.objects.get(sizes=size_id)
                    image = ItemImages.objects.filter(cloth_item=item).first()
                    items_data.append({
                        'item': item,
                        'size': size,
                        'quantity': quantity,
                        'image': image
                    })

            context = {
                'user': user,
                'items_data': items_data,
                'quantity_range': range(1, 6),
                'cart_items': cart_items
            }
            return render(request, 'user-order.html', context)
        return redirect(request.META.get('HTTP_REFERER'))

    else:
        return redirect('/userlogin')


def show_cart(request):
    if 'username' in request.session:
        user_name = request.session['username']
        user = User.objects.get(username=user_name)
        cart_items = Cart.objects.filter(user=user.user_id)
        wishlists = Wishlist.objects.filter(user=user.user_id)
        overall_total = 0
        overall_tax = 0
        for item in cart_items:
            item.tax = item.quantity * 10
            overall_tax += item.tax
            item.total_price = item.quantity * item.cloth_item.price
            overall_total += item.total_price + item.tax
        return render(request, 'user-cart.html', {'cart_items': cart_items,
                                                  "wishlist": wishlists,
                                                  'overall_total': overall_total,
                                                  'overall_tax': overall_tax,
                                                  'quantity_range': range(1, 6)})
    else:
        return redirect('/userlogin')


def show_user_profile(request):
    username = request.session['username']
    user = User.objects.get(username=username)
    gender_choices = User.GENDER_CHOICES
    wishlist = Wishlist.objects.filter(user=user)
    district = District.objects.all().order_by('district_name')
    state = State.objects.all().order_by('state_name')
    print('hi')
    print(user)
    order_items = OrderItems.objects.filter(order__user_id=user.user_id)
    print(order_items)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update-profile-pic':
            if 'profilepic' in request.FILES:
                user.profile_pic = request.FILES.get('profilepic')
                user.save()
            else:
                pass
        elif action == 'update-address':
            firstname = request.POST.get('firstname')
            secondname = request.POST.get('secondname')
            email = request.POST.get('email')
            phno = request.POST.get('phno')
            district_id = request.POST.get('district')
            district_new = District.objects.get(district_id=district_id)
            state = request.POST.get('state')
            gender = request.POST.get('gender')
            address = request.POST.get('address')
            pincode = request.POST.get('pincode')

            user.firstname = firstname
            user.secondname = secondname
            user.email = email
            user.gender = gender
            user.ph_no = phno
            user.save()

            Address.objects.create(user=user, district=district_new, address=address, pin_code=pincode)

    return render(request, 'user-profile.html', {'user': user,
                                                 "gender_choices": gender_choices,
                                                 "wishlist": wishlist,
                                                 "district": district,
                                                 "state": state,
                                                 "orderitems": order_items})


def change_profile_pic(request):
    username = request.session['username']
    user = User.objects.get(username=username)
    if request.method == 'POST':
        user.profile_pic = request.FILES.get('profilepic')
        user.save()
    return redirect('/user-profile')


def add_to_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        size_id = request.POST.get('size_id')
        if size_id == 0:
            return JsonResponse({'message': 'please select a size'})
        else:
            try:
                size = Size.objects.get(size_id=size_id)
                user = request.session['username']
                if user:
                    user1 = User.objects.get(username=user)
                    cloth_item = ClothItems.objects.get(item_id=item_id)

                    try:
                        in_cart = Cart.objects.get(cloth_item=item_id, user=user1)

                        if in_cart:
                            return JsonResponse({'message': 'item already in cart'})
                        else:
                            new_cart_item = Cart.objects.create(user=user1, cloth_item=cloth_item, size=size)
                    except Cart.DoesNotExist:
                        new_cart_item = Cart.objects.create(user=user1, cloth_item=cloth_item, size=size)
                    return JsonResponse({'message': 'success'})
                else:
                    return JsonResponse({'message': 'user not authenticated'}, status=401)
            except Size.DoesNotExist:
                return JsonResponse({'message': 'please select a size'})
            except ValueError:
                return JsonResponse({'message': 'please select a size'})
    return JsonResponse({'message': 'Failed'}, status=400)


def updatequantity(request):
    if 'username' in request.session:
        username = request.session['username']
        user = User.objects.get(username=username)
        if request.method == 'POST':
            clothid = request.POST['cloth_id']
            quantity = request.POST['qty']
            try:
                cart_item = Cart.objects.get(user=user, cloth_item=clothid)
                cart_item.quantity = quantity
                cart_item.save()
            except Cart.DoesNotExist:
                pass

            return JsonResponse({'message': 'qty updated'})
        else:
            return JsonResponse({'message': 'not updated'})

    else:
        return redirect('/userlogin')


def update_address(request):
    if request.method == "POST":
        name = request.session.get('username')
        user = User.objects.get(username=name)

        # Get address data from form
        phone = request.POST.get('phone')
        pincode = request.POST.get('pincode')
        state = request.POST.get('state')
        address = request.POST.get('address')
        print(f"Phone: {phone}, Pincode: {pincode}, State: {state}, Address: {address}")

        if not address:
            messages.error(request, 'Address cannot be empty.')
            return redirect(request.META.get('HTTP_REFERER'))

        # Update user address
        address_instance = user.my_address.first()
        address_instance.address = address
        address_instance.pin_code = pincode
        address_instance.district.district_name = state  # Assuming the district name is updated in the address
        address_instance.save()

        # Optionally, update user's phone number as well
        user.ph_no = phone
        user.save()

        # Redirect back to the user-order page with updated user information
        return redirect(request.META.get('HTTP_REFERER'))

    # In case of GET request or other method, redirect to some default page or handle errors
    return redirect('default_page')


# def confirm_order(request):
#     username = request.session['username']
#     user = User.objects.get(username = username)
#     if request.method == 'POST':
#         item_name = request.POST.get('clothname')
#         item_size = request.POST.get('size')
#         item_price = request.POST.get('price')
#         item_quantity = request.POST.get('quantity')
#         user_address = request.POST.get('address')
#         print(item_name,item_size,item_quantity,item_price,user_address)
#
#         item = ClothItems.objects.get(item_name = item_name)
#         item_total_price = int(item_quantity) * item.price
#         item_size = Size.objects.get(sizes=item_size)
#         print(item,item_size,item_total_price)
#
#         order_instance = Order()
#
#         order_instance.user = user
#         order_instance.total_price = item_total_price
#         order_instance.status = 'pending'
#         order_instance.shipping_address = user_address
#         order_instance.payment_status = 'paid'
#         order_instance.save()
#
#         order_item_instance = OrderItems()
#
#         order_item_instance.order = order_instance
#         order_item_instance.cloth_item = item
#         order_item_instance.quantity = int(item_quantity)
#         order_item_instance.price = int(item_price)
#         order_item_instance.total_price = int(item_total_price)
#         order_item_instance.save()
#
#         return render(request,'order-confirm.html')


from django.conf import settings


def confirm_order(request):
    username = request.session['username']
    user = User.objects.get(username=username)
    cart_items = Cart.objects.filter(user=user.user_id)
    if request.method == 'POST':
        order_instance = Order(
            user=user,
            status='pending',
            shipping_address=request.POST.get('address'),
            payment_status='paid'
        )
        order_instance.save()

        items = []
        item_names = request.POST.getlist('clothname')
        sizes = request.POST.getlist('size')
        prices = request.POST.getlist('price')
        quantities = request.POST.getlist('quantity')

        total_order_price = 0

        for item_name, item_size, item_price, item_quantity in zip(item_names, sizes, prices, quantities):
            item = ClothItems.objects.get(item_name=item_name)
            item_size_obj = Size.objects.get(sizes=item_size)
            item_total_price = int(item_quantity) * int(item_price)

            # update total price
            total_order_price += item_total_price

            # reduce the count of stock from cloth item
            item.stock = int(item.stock) - int(item_quantity)

            order_item_instance = OrderItems.objects.create(
                order=order_instance,
                cloth_item=item,
                size=item_size_obj,
                quantity=int(item_quantity),
                price=int(item_price),
                total_price=item_total_price,
                status= 'pending'
            )


            #order_id passing
            order_id = order_instance.order_id

            # add item to the items list
            items.append({
                'item_name': item.item_name,
                'size': item_size,
                'quantity': item_quantity,
                'price': item_price
            })

        # update the total price in order instance
        order_instance.total_price = total_order_price
        order_instance.save()

        # payment
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create({
            'amount': total_order_price * 100,
            'currency': 'INR',
            'payment_capture': '1'
        })
        razorpay_order_id = razorpay_order['id']
        razorpay_order['name'] = user.user_id
        razorpay_order['order'] = order_instance.order_id
        price = razorpay_order['amount']

        PaymentModel.objects.create(
            user=user, order=order_instance, razorpay_order_id=razorpay_order_id, amount=price)

        return render(request, 'order-summary.html', {'items': items,
                                                      'cart_items': cart_items,
                                                      'payment': razorpay_order, 'username': username,
                                                      'order_id': order_id})


@csrf_exempt
def payment_handler(request, order, user):
    order_id = Order.objects.get(order_id=order)
    user = User.objects.get(user_id=user)

    if request.method == 'POST':
        payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        try:
            # username = request.session.get('username')
            # user = User.objects.get(username=username)
            # order = Order.objects.get(order_id=order_id)

            payment = PaymentModel(
                user=user,
                order=order_id,
                razorpay_order_id=razorpay_order_id,
                razorpay_id=payment_id,
                paid=True
            )
            payment.save()

            return render(request, 'order-confirm.html', {'payment_id': payment_id})

        except Exception as e:
            print(f"Error: {e}")
            return HttpResponseBadRequest("Invalid payment request")


def delete_order_item(request, id, orderid):
    if request.method == 'POST':
        item = OrderItems.objects.get(cloth_item=id, order_items_id=orderid)
        item.status = 'cancelled'
        item.save()
    return redirect('/user-profile')
