from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE, default="Pansamantala")
    username = models.CharField(max_length=150, unique=True, default="Pansamantala")
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    mi = models.CharField(max_length=1)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    region = models.CharField(max_length=200, default='Unknown')
    province = models.CharField(max_length=200, default='Unknown')
    municipality = models.CharField(max_length=200, default='Unknown')
    barangay = models.CharField(max_length=200, default='Unknown')
    street = models.CharField(max_length=200, default='Unknown')
    profile_pic = models.ImageField(default="dflt.jpg", null=True, blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

# Create your models here.
'''
working to 
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
'''







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
    
class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
        ('Order Rejected', 'Order Rejected'),
        ('Processing', 'Processing'),
        ('Ready for pickup', 'Ready for pickup'),
    )
    is_hidden = models.BooleanField(default=False)
    id = models.AutoField(primary_key=True)  # Add primary key field with auto-increment
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    color = models.ForeignKey(Color, null=True, on_delete=models.SET_NULL)  # Add the color field
    fabric = models.ForeignKey(Fabric, null=True, on_delete=models.SET_NULL)  # Add the fabric field
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=235, null=True, choices=STATUS)
    note = models.CharField(max_length=1000, null=True)

    def order_id(self):
        return f"Order_ID#{self.id:03d}"  # Generate the order ID with prefix and zero-padding

    def __str__(self):
         return self.order_id()