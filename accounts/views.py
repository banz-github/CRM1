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
from .forms import OrderFormU
from django.shortcuts import render, get_object_or_404


'''
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
'''
from django.contrib.auth.decorators import login_required

@unathenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            customer_group = Group.objects.get(name='customer')
            customer_group.user_set.add(user)  # Assign user to the "customer" group

            Customer.objects.create(
                user=user,
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                mi=form.cleaned_data['mi'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone']
            )

            messages.success(request, 'Account was created successfully')
            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)




@unathenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
     logout(request)
     return redirect('login')
''' working
@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.filter(is_hidden=False)
    customer = Customer.objects.all()

    total_customers = customer.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    # Add counts for the new statuses
    rejected = orders.filter(status='Order Rejected').count()
    processing = orders.filter(status='Processing').count()
    out_for_delivery = orders.filter(status='Out for delivery').count()

    context = {
        'orders': orders,
        'customer': customer,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending,
        'rejected': rejected,
        'processing': processing,
        'out_for_delivery': out_for_delivery,
    }
    return render(request, 'accounts/dashboard.html', context)
'''
from django.db.models import Q

@login_required(login_url='login')
@admin_only
def home(request):
    query = request.GET.get('q')
    orders = Order.objects.filter(is_hidden=False)

    if query:
        # Filter by related Customer fields using '__' to navigate the ForeignKey relationship
        orders = orders.filter(
            Q(customer__first_name__icontains=query) |
            Q(customer__last_name__icontains=query) |
            Q(id__icontains=query) |  # Search by primary key (order ID)
            Q(product__name__icontains=query) |  # Filter based on the 'name' field of the Product model
            Q(fabric__name__icontains=query) |  # Filter based on the 'name' field of the Fabric model
            Q(color__name__icontains=query) |  # Filter based on the 'name' field of the Color model
            Q(customer__municipality__icontains=query) |
            Q(customer__barangay__icontains=query) |
            Q(customer__street__icontains=query) |
            Q(customer__email__icontains=query) |
            Q(customer__phone__icontains=query) |
            Q(date_created__icontains=query) |
            Q(status__icontains=query) |
            Q(customer__id__icontains=query)  # Search by customer ID (ForeignKey field)
        )

    customer = Customer.objects.all()
    total_customers = customer.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    rejected = orders.filter(status='Order Rejected').count()
    processing = orders.filter(status='Processing').count()
    out_for_delivery = orders.filter(status='Out for delivery').count()

    context = {
        'orders': orders,
        'customer': customer,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending,
        'rejected': rejected,
        'processing': processing,
        'out_for_delivery': out_for_delivery,
        'search_query': query,
    }
    return render(request, 'accounts/dashboard.html', context)

from django.db.models import Count
# ... (Previous code)
# ... (Previous code)

from django.db.models import Count

@login_required(login_url='login')
@admin_only
def dashboardAnalytics(request):
    # Most Ordered Product
    most_ordered_product = Order.objects.values('product__name').annotate(count=Count('product__name')).order_by('-count')[:5]
    most_ordered_product_labels = [item['product__name'] for item in most_ordered_product]
    most_ordered_product_counts = [item['count'] for item in most_ordered_product]

    # Most Ordered Color
    most_ordered_color = Order.objects.values('color__name').annotate(count=Count('color__name')).order_by('-count')[:5]
    most_ordered_color_labels = [item['color__name'] for item in most_ordered_color]
    most_ordered_color_counts = [item['count'] for item in most_ordered_color]

    # Most Ordered Fabric
    most_ordered_fabric = Order.objects.values('fabric__name').annotate(count=Count('fabric__name')).order_by('-count')[:5]
    most_ordered_fabric_labels = [item['fabric__name'] for item in most_ordered_fabric]
    most_ordered_fabric_counts = [item['count'] for item in most_ordered_fabric]

    # Top Customer
    top_customers = Customer.objects.annotate(order_count=Count('order')).order_by('-order_count')[:5]
    top_customer_labels = [f"{customer.first_name} {customer.last_name}" for customer in top_customers]
    top_customer_order_counts = [customer.order_count for customer in top_customers]

    # Address with Most Orders
    most_ordered_addresses = Customer.objects.annotate(order_count=Count('order')).order_by('-order_count')[:5]
    most_ordered_address_labels = [f"{customer.municipality}, {customer.barangay}, {customer.street}" for customer in most_ordered_addresses]
    most_ordered_address_counts = [customer.order_count for customer in most_ordered_addresses]

    context = {
        'most_ordered_product_labels': most_ordered_product_labels,
        'most_ordered_product_counts': most_ordered_product_counts,
        'most_ordered_color_labels': most_ordered_color_labels,
        'most_ordered_color_counts': most_ordered_color_counts,
        'most_ordered_fabric_labels': most_ordered_fabric_labels,
        'most_ordered_fabric_counts': most_ordered_fabric_counts,
        'top_customer_labels': top_customer_labels,
        'top_customer_order_counts': top_customer_order_counts,
        'most_ordered_address_labels': most_ordered_address_labels,
        'most_ordered_address_counts': most_ordered_address_counts,
    }
    return render(request, 'accounts/dashboard_analytics.html', context)

@login_required(login_url='login')
@admin_only 
def view_customers(request):
    customer = Customer.objects.all()


    context = {
        'customer':customer
    }
    return render(request, 'accounts/view_customers.html', context)

from django.core.exceptions import ObjectDoesNotExist #Error catching
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    customer = request.user.customer
    try:
        latest_order = customer.order_set.latest('date_created')
    except ObjectDoesNotExist:
        # Handle the case when no order exists for the customer
        latest_order = None
    context = {
        'latest_order': latest_order,
    }

    return render(request, 'accounts/user.html', context)

# views.py
from django.shortcuts import render, get_object_or_404
from .models import Order

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order,
    }
    return render(request, 'accounts/order.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def myordersPage(request):

    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    
    # Add counts for the new statuses
    rejected = orders.filter(status='Order Rejected').count()
    processing = orders.filter(status='Processing').count()
    out_for_delivery = orders.filter(status='Out for delivery').count()
    print('ORDERS:',orders)

    context = {
        'orders': orders,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending,
        'rejected': rejected,
        'processing': processing,
        'out_for_delivery': out_for_delivery,
    }

    return render(request, 'accounts/myorders.html', context)
''' Working di lang nagana ung changes sa user
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
'''

from django.db.models.signals import post_save
from django.dispatch import receiver

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    # Signal to update the associated user's email when the customer's email changes
    @receiver(post_save, sender=Customer)
    def update_user_email(sender, instance, created, **kwargs):
        if not created:  # Only update user email if the Customer instance already exists (not created in this signal)
            instance.user.email = instance.email
            instance.user.save()

    context = {'form': form}
    return render(request, 'accounts/account_settings.html', context)


from django import forms

class PhoneForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone']

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def providePhone(request):
    customer = request.user.customer
    form = PhoneForm(instance=customer)

    if request.method == 'POST':
        form = PhoneForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'accounts/force_phonenum.html', context)


@login_required(login_url='provide_phone')
def providePhonePage(request):
    if request.method == 'POST':
        form = PhoneForm(request.POST, instance=request.user.customer)
        if form.is_valid():
            form.save()
            return redirect('user_home')  # Redirect to the main user page
    else:
        form = PhoneForm(instance=request.user.customer)

    context = {'form': form}
    return render(request, 'accounts/provide_phone.html', context)


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
    
    total_orders = orders.count()
    context = {
        'orders': orders,
        'total_orders': total_orders
    }
    return render(request, 'accounts/hidden_orders.html', context)

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
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
         form = OrderForm(request.POST, instance=order)
    if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
     order = Order.objects.get(id=pk)
     if request.method == "POST":
          order.delete()
          return redirect('/')
     context = {'item':order}
     return render(request, 'accounts/delete.html', context)
'''
######################################


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

###################
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def createOrderU(request):
    customer = request.user.customer

    if request.method == 'POST':
        form = OrderFormU(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = customer
            order.status = 'Pending'
            order.is_hidden = 0  # Set is_hidden to 0 (not hidden)
            order.save()
            return redirect('user-page')  # Update the redirect statement to 'user-page'

    else:
        form = OrderFormU()

    context = {'form': form}
    return render(request, 'accounts/create_orderU.html', context)





################# color views
from .models import Color

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def colors(request):
    colors = Color.objects.all()
    return render(request, 'accounts/colors.html', {'colors': colors})



from .forms import ColorForm


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def add_color(request):
    if request.method == 'POST':
        form = ColorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('colors')
    else:
        form = ColorForm()

    context = {'form': form}
    return render(request, 'accounts/add_color.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_color(request, color_id):
    color = Color.objects.get(id=color_id)

    if request.method == 'POST':
        form = ColorForm(request.POST, instance=color)
        if form.is_valid():
            form.save()
            return redirect('colors')
    else:
        form = ColorForm(instance=color)

    context = {'form': form}
    return render(request, 'accounts/update_color.html', context)

def delete_color(request, color_id):
    color = Color.objects.get(id=color_id)
    if request.method == 'POST':
        color.delete()
        return redirect('colors')
    return render(request, 'accounts/confirm_color_delete.html', {'color': color})




############ FABRIC
from .models import Fabric

def fabrics(request):
    fabrics = Fabric.objects.all()
    return render(request, 'accounts/fabrics.html', {'fabrics': fabrics})

def add_fabric(request):
    if request.method == 'POST':
        name = request.POST['name']
        price_per_yard = request.POST['price_per_yard']
        # Handle tags

        fabric = Fabric.objects.create(name=name, price_per_yard=price_per_yard)
        # Add fabric to tags

        return redirect('fabrics')

    return render(request, 'accounts/add_fabric.html')

def update_fabric(request, fabric_id):
    fabric = Fabric.objects.get(id=fabric_id)

    if request.method == 'POST':
        fabric.name = request.POST['name']
        fabric.price_per_yard = request.POST['price_per_yard']
        # Handle tags

        fabric.save()
        # Update fabric tags

        return redirect('fabrics')

    return render(request, 'accounts/update_fabric.html', {'fabric': fabric})

def delete_fabric(request, fabric_id):
    fabric = Fabric.objects.get(id=fabric_id)

    if request.method == 'POST':
        fabric.delete()
        # Remove fabric from tags

        return redirect('fabrics')

    return render(request, 'accounts/delete_fabric.html', {'fabric': fabric})



############ LANDING RELATED
@unathenticated_user
def landingPage(request):



    context = {

    }
    return render(request, 'accounts/landing_page.html', context)