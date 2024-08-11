from django.db import models

# Create your models here.

class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_username = models.CharField(max_length=100, unique=True)
    admin_mail = models.EmailField(unique=True)
    admin_password = models.CharField(max_length=100)


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100,unique=True)
    category_img = models.ImageField(upload_to='images/', null=True)

    def __str__(self):
        return self.category_name

class ClothItems(models.Model):
    item_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='category')
    item_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    stock = models.IntegerField()


class Size(models.Model):
    size_id = models.AutoField(primary_key = True)
    sizes = models.CharField(max_length=100)
    def __str__(self):
        return self.sizes


class ClothSpecification(models.Model):
    item_spec_id = models.AutoField(primary_key = True)
    cloth_item = models.ForeignKey(ClothItems, on_delete=models.CASCADE, related_name='size')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True)


class ItemImages(models.Model):
    image_id = models.AutoField(primary_key=True)
    cloth_item = models.ForeignKey(ClothItems, on_delete=models.CASCADE, related_name='images')
    image_url = models.ImageField(upload_to='images/')


class State(models.Model):
    state_id = models.AutoField(primary_key=True)
    state_name = models.CharField(max_length=100)


class District(models.Model):
    district_id = models.AutoField(primary_key=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    district_name = models.CharField(max_length=100)
