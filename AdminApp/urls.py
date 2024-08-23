from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),

    # path('adminLogin/', views.),
    path('adminSignup/', views.register),
    # path('logout/', views.admin_logout),

    path('', views.home),

    path('add-category/',views.add_category),
    path('deleteCategory/<int:id>',views.delete_category),
    path('updateCategory/<int:id>',views.update_category),
    path('category/',views.view_category),

    path('add-product/',views.add_product),
    path('products/',views.view_product),
    path('viewallproducts',views.view_product),
    path('first/category/<int:id>',views.view_products_categorize),


    path('order-list/',views.order_list),
    path('order-list/order-details',views.order_details),

    path('transaction-list/',views.transaction_list),
    path('transaction-list/transaction-details/',views.transaction_details),

    path('profile',views.profile)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
