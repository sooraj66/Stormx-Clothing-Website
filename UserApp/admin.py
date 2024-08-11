from django.contrib import admin
from .models import User, Wishlist,Cart

# Register your models here.

admin.site.register(User)
admin.site.register(Wishlist)
admin.site.register(Cart)
