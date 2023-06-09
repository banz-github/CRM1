from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login,logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
# Create your views here. 
from .models import *
from .models import Customer
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from .decorators import unathenticated_user, allowed_users, admin_only
###############
from .forms import ProductForm

from django.shortcuts import render, get_object_or_404
from .models import Order, ArchivedOrder
from datetime import datetime

@unathenticated_user
def registerPage(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

        
    context = {'form':form}
    return render(request, 'accounts/register.html', context)


@unathenticated_user
def loginPage(request):

        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect.')

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
     logout(request)
     return redirect('login')

@login_required(login_url='login')
@admin_only 
def home(request):
    orders = Order.objects.filter(is_hidden=False)  # Filter out hidden orders
    customer = Customer.objects.all()

    total_customers = customer.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {
        'orders': orders,
        'customer': customer,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):

    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    
    print('ORDERS:',orders)

    context = {
        'orders': orders,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending
    }

    return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()


    context = {'form':form}
    return render(request, 'accounts/account_settings.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request): # 3
    products = Product.objects.all()
    return render(request,'accounts/products.html', {'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders = customer.order_set.filter(is_hidden=False)
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {
        'customer': customer,
        'orders': orders,
        'order_count': order_count,
        'myFilter': myFilter
    }
    return render(request, 'accounts/customer.html', context)


def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    # Additional logic for the customer detail page
    return render(request, 'accounts/customer_detail.html', {'customer': customer})

'''
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    #form = OrderForm(initial={'customer': customer})
    if request.method == 'POST':
        #print('Printing POST:',request.POST)
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('customer-detail', pk=customer.id)


    context = {'formset':formset}
    return render(request, 'accounts/order_form.html', context)

'''
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request):
    form = OrderForm()
    if request.method == 'POST':
        #print('Printing POST:', request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)

from .models import Order, ArchivedOrder

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def archivedOrders(request):
    archived_orders = ArchivedOrder.objects.all()
    context = {'archived_orders': archived_orders}
    return render(request, 'accounts/archived_orders.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def archived_orders(request):
    archived_orders = ArchivedOrder.objects.all()
    return render(request, 'accounts/archived_orders.html', {'archived_orders': archived_orders})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrderC(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            orders = formset.save(commit=False)
            for order in orders:
                order.is_hidden = False  # Set is_hidden to 0 (False) by default
                order.save()
            return redirect('/')

    context = {'formset': formset}
    return render(request, 'accounts/order_formC.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        #print('Printing POST:', request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)

####################### THIS WILL LITERALLY DELETE THE ORDER 
'''
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'item':order}
    return render(request, 'accounts/delete.html', context)
#######################################
@login_required(login_url='login')
@admin_only 
def hidden_orders(request):
    orders = Order.objects.filter(is_hidden=True)  # Filter hidden orders
    return render(request, 'accounts/hidden_orders.html', {'orders': orders})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def toggle_order_hidden(request, order_id):
    order = Order.objects.get(id=order_id)

    # Toggle the value of is_hidden field
    order.is_hidden = not order.is_hidden
    order.save()

    return redirect('home')
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def unhide_order(request, pk):
    order = Order.objects.get(id=pk)
    order.is_hidden = False
    order.save()
    return redirect('hidden_orders')


'''

############# NEW DELETE FUNCTIONALITY (ARCHIVED)
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        # Create an archived order object and populate its fields
        archived_order = ArchivedOrder(order=order)
        archived_order.archived_date = datetime.now()  # Set the archived date/time
        archived_order.save()
        
        # Delete the order
        order.delete()
        
        return redirect('/')
    
    context = {'item': order}
    return render(request, 'accounts/delete.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def archiveOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        # Create an archived order object and populate its fields
        archived_order = ArchivedOrder(order=order)
        archived_order.archived_date = datetime.now()  # Set the archived date/time
        archived_order.save()
        
        # Update the is_archived field of the order
        order.is_archived = True
        order.save()
        
        return redirect('/')
  
    
    context = {'item': order}
    
    return render(request, 'accounts/archive.html', context)
    




@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = ProductForm()

    context = {'form': form}
    return render(request, 'accounts/add_product.html', context)
#################
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    return redirect('products')  # Redirect to the product listing page
########################
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_product(request, product_id):
    product = Product.objects.get(id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = ProductForm(instance=product)

    context = {'form': form}
    return render(request, 'accounts/update_product.html', context)

