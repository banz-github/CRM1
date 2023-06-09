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
    )
<<<<<<< HEAD
    is_hidden = models.BooleanField(default=False)
    id = models.AutoField(primary_key=True)  # Add primary key field with auto-increment
=======

    id = models.AutoField(primary_key=True)
>>>>>>> faaeb49dc135aa7d509eba53888f5fa6be0b7334
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=235, null=True, choices=STATUS)
    note = models.CharField(max_length=1000, null=True)
    is_archived = models.BooleanField(default=False)  # Add a field to indicate if the order is archived

    def order_id(self):
        return f"Order_ID#{self.id:03d}"

    def __str__(self):
        return self.order_id()

class ArchivedOrder(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, primary_key=True)
    archived_date = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=235, null=True)
    note = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return str(self.order)




