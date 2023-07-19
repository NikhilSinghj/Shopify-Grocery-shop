from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass
    


class Category(models.Model):
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True)    
    category_id=models.IntegerField(unique=True,null=True)
    category_name=models.CharField(max_length=20)
    category_image=models.ImageField(upload_to='images')
    category_added_date=models.DateTimeField(auto_now_add=True)
    category_deleted_date=models.DateTimeField(null=True,blank=True)
    category_edited_date=models.DateTimeField(null=True,blank=True)
    deleted_status=models.CharField(max_length=20,default=False)



ITEM_CHOICES=(
    ("PER GK","/kg"),
    ("PER LETRE","/ltr"),
    ("PER QTY","/qty")
)

class Items(models.Model):
    items=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    product_category=models.ForeignKey(Category,on_delete=models.DO_NOTHING)
    pruduct_name=models.CharField(max_length=30)
    price=models.FloatField()
    unit=models.CharField(max_length=10,choices=ITEM_CHOICES,default="PER QTY")
    image=models.ImageField(upload_to='images')
    product_quantity=models.IntegerField()
    product_added_date=models.DateTimeField(auto_now_add=True)
    product_expiry_date=models.DateField(null=True,blank=True)
    description=models.TextField(max_length=200)
    deleted_status=models.BooleanField(default=False)


class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    item=models.ForeignKey(Items,on_delete=models.DO_NOTHING)
    orderd=models.BooleanField(default=False)
    pruduct_name=models.CharField(max_length=30)
    ordered_quantity=models.IntegerField(default=0)
    added_to_cart=models.BooleanField(default=False)
    purchased=models.BooleanField(default=False)






