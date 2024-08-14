from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home',views.home),
    path('userlogin/',views.user_login),
    path('usersignup/',views.user_signup),
    path('userlogout',views.user_logout),
    path('category/<int:id>',views.show_products),
    path('deletefromcart/<int:id>',views.deletefromcart),
    path('<int:catid>/<int:itmid>',views.add_to_wishlist),
    path('deletefromwishlist/<int:id>',views.deletefromwishlist),
    path('<str:category>/<int:id>',views.produt_description, name='product_description'),
    path('delete/<int:id>',views.deletefromwishlist),
    path('order',views.show_order,name ='show_order' ),
    path('cart',views.show_cart),
    path('user-profile',views.show_user_profile),
    path('add-to-cart',views.add_to_cart),
    path('updateQuantity',views.updatequantity),
    path('update_address', views.update_address, name='update_address'),
    path('confirm-order',views.confirm_order,name='confirm_order')
    # path('buy-now/<int:item_id>/', views.buy_now, name='buy_now'),
    # path('changeprofilepic',views.change_profile_pic)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
