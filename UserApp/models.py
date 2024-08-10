from django.db import models
from AdminApp.models import ClothItems,District

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
    signup_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, default='active')


class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    address = models.CharField(max_length=300)
    pin_code = models.IntegerField()


class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cloth_item = models.ForeignKey(ClothItems, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)


class Wishlist(models.Model):
    wishlist_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="user")
    cloth_item = models.ForeignKey(ClothItems, on_delete=models.CASCADE,related_name="clothitem")

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cloth_item = models.ForeignKey(ClothItems, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review_text = models.TextField()