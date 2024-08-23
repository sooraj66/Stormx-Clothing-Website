from django.contrib import admin
from .models import User, Wishlist,Cart, Order,OrderItems, PaymentModel

# Register your models here.

admin.site.register(User)
admin.site.register(Wishlist)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItems)
admin.site.register(PaymentModel)

