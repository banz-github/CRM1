from django.contrib import admin

# Register your models here.
from .models import *
from .models import Order
from .models import Color

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'product', 'date_created', 'status')  # Specify the fields to display

    def order_id(self, obj):
        return obj.order_id()  # Display the formatted order ID

    list_filter = ('status',)
    search_fields = ('product__name', 'customer__name')  # Search by product name or customer name
    list_per_page = 20  # Number of orders displayed per page


admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(Order, OrderAdmin)
admin.site.register(Color)
