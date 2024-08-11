from django.contrib import admin
from .models import ClothItems,Category,District,State,ItemImages,ClothSpecification,Admin

# Register your models here.

# admin.py
from django.contrib import admin
from .models import Category, ClothItems, ClothSpecification, ItemImages,Size

class ClothSpecificationInline(admin.TabularInline):
    model = ClothSpecification
    extra = 1  # Number of extra forms to display

class ItemImagesInline(admin.TabularInline):
    model = ItemImages
    extra = 1  # Number of extra forms to display

class ClothItemsAdmin(admin.ModelAdmin):
    inlines = [ClothSpecificationInline, ItemImagesInline]
    list_display = ('item_name', 'category', 'price', 'stock')
    search_fields = ('item_name',)


admin.site.register(Category)
admin.site.register(ClothItems, ClothItemsAdmin)
admin.site.register(Size)




