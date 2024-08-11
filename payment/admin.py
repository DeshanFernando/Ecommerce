from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem

admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

# create an OrderItem inline
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

# extend our Order model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered"]
    fields = ["user", "full_name", "email", "address", "amount_paid", "date_ordered", "shipped", "date_shipped"]
    inlines = [OrderItemInline]

# unregister Order model
admin.site.unregister(Order)

# re-register Order and OrderAdmin models
admin.site.register(Order, OrderAdmin)
