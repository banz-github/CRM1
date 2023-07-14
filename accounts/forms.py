from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *
from .models import Product
from django import forms
from .models import Order

class AccountSettingsForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        

class CustomerForm(forms.ModelForm):
    # Fields from the Customer model
    # ...

    # Fields from the Address model
    region = forms.CharField()
    province = forms.CharField()
    municipality = forms.CharField()
    barangay = forms.CharField()
    street = forms.CharField()

    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    mi = forms.CharField(required=True)
    phone = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'mi', 'phone']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class OrderFormU(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['status'] = 'Pending'


class ColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = '__all__'
