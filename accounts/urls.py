from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

from django.conf.urls.static import static
from django.conf import settings
from .views import add_product




urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    

    path('', views.home, name="home"),
    path('user/', views.userPage, name="user-page"),
    path('account/', views.accountSettings, name="account"),

    path('products/', views.products, name="products"),
    path('customer/<str:pk_test>/', views.customer, name="customer"),

    path('create_order/', views.createOrder, name="create_order"),
    path('create_orderC/<str:pk>/', views.createOrderC, name="create_orderC"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),



    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), name="reset_password"),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), name="password_reset_done"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), name="password_reset_confirm"),
    
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), name="password_reset_complete"),
#############
    path('add_product/', add_product, name='add_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('update_product/<int:product_id>/', views.update_product, name='update_product'),

     path('customer/<int:pk>/', views.customer_detail, name='customer-detail'),

    path('view_customers/', views.view_customers, name='view_customers'),
    

    path('hidden_orders/', views.hidden_orders, name='hidden_orders'),
    path('toggle_order_hidden/<int:order_id>/', views.toggle_order_hidden, name='toggle_order_hidden'),
    path('unhide_order/<int:pk>/', views.unhide_order, name='unhide_order'),
    path('user/create_orderU/', views.createOrderU, name='create_orderU'),
    path('providephone/', views.providePhone, name='providephone'),
    path('provide-phone/', views.providePhonePage, name='provide_phone'),

    ###### color 
    path('add_color/', views.add_color, name='add_color'),
    path('colors/', views.colors, name='colors'),
    path('update_color/<int:color_id>/', views.update_color, name='update_color'),
    path('delete_color/<int:color_id>/', views.delete_color, name='delete_color'),
    ########## frabric
    path('fabrics/', views.fabrics, name='fabrics'),
    path('add_fabric/', views.add_fabric, name='add_fabric'),
    path('update_fabric/<int:fabric_id>/', views.update_fabric, name='update_fabric'),
    path('delete_fabric/<int:fabric_id>/', views.delete_fabric, name='delete_fabric'),

]
    

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)