from django.db import models
from AdminApp.models import ClothItems,District,Size

# Create your models here.
class User(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    user_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=200,null=True)
    secondname = models.CharField(max_length=200,null=True)
    username = models.CharField(max_length=200, unique=True)
    gender = models.CharField(max_length=20,choices=GENDER_CHOICES,null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    profile_pic = models.FileField(upload_to='profile_pics/',blank=True,null=True)
    ph_no = models.CharField(max_length=20, null=True)
    signup_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, default='active')


class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'my_address')
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    address = models.CharField(max_length=300)
    pin_code = models.IntegerField()


class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cloth_item = models.ForeignKey(ClothItems, on_delete=models.CASCADE,related_name='clothitemcart')
    size = models.ForeignKey(Size,on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField(null=True,default=1)


class Wishlist(models.Model):
    wishlist_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="user")
    cloth_item = models.ForeignKey(ClothItems, on_delete=models.CASCADE,related_name="clothitem")

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_orders')
    total_price = models.IntegerField(null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,null=True)
    shipping_address = models.CharField(max_length=100,null=True)
    payment_status = models.CharField(max_length=10,null=True)

class OrderItems(models.Model):
    order_items_id = models.AutoField(primary_key = True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    cloth_item = models.ForeignKey(ClothItems,on_delete=models.CASCADE)
    size = models.CharField(max_length=10,null=True)
    quantity = models.IntegerField()
    price = models.IntegerField()
    total_price = models.IntegerField()



class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cloth_item = models.ForeignKey(ClothItems, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review_text = models.TextField()