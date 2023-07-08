from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    id = models.AutoField(primary_key=True)  # Add primary key field with auto-increment
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="dflt.jpg", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    id = models.AutoField(primary_key=True)  # Add primary key field with auto-increment
    CATEGORY = (
        ('Residential', 'Residential'),
        ('Commercial', 'Commercial'),
        ('Auto', 'Auto'),
    )

    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name if self.name is not None else ''



'''
class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Ready to be picked-up', 'Ready to be picked-up'),
        ('Order Rejected', 'Order Rejected'),
    )
    customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    #note = models.CharField(max_length=1000, null=True)
    def __str__(self):
        if self.product:
            return str(self.product.name)
        return f"No Product (Order #{self.id})"
'''

class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
        ('Order Rejected', 'Order Rejected'),
        ('Processing', 'Processing'),
    )
    is_hidden = models.BooleanField(default=False)
    id = models.AutoField(primary_key=True)  # Add primary key field with auto-increment
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=235, null=True, choices=STATUS)
    note = models.CharField(max_length=1000, null=True)

    def order_id(self):
        return f"Order_ID#{self.id:03d}"  # Generate the order ID with prefix and zero-padding

    def __str__(self):
         return self.order_id()
    



####### new

class Color(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, default="")  # Add the code field

    def __str__(self):
        return self.name


class Fabric(models.Model):
    id = models.AutoField(primary_key=True)
    CATEGORY = (
        ('Residential', 'Residential'),
        ('Commercial', 'Commercial'),
        ('Auto', 'Auto'),
    )

    name = models.CharField(max_length=200, null=True)
    price_per_yard = models.FloatField(null=True)
    tags = models.ManyToManyField(Tag)
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name if self.name is not None else ''
