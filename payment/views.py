from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

from cart.cart import Cart
from payment.forms import ShippingForm, BillingForm
from payment.models import ShippingAddress, Order, OrderItem
from store.models import Product

def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, "payment/shipped_dash.html")
    else:
        messages.success(request, "Access Denied")
        return redirect('/')


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, "payment/not_shipped_dash.html")
    else:
        messages.success(request, "Access Denied")
        return redirect('/')

def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants
        totals = cart.cart_total()
        
        # get billing from the last page
        billing_form = BillingForm(request.POST or None)

        # Get shipping session data
        my_shipping = request.session['my_shipping']
        # Gather order info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}\n"
        amount_paid = totals

        # Create an order
        if request.user.is_authenticated:
             user = request.user
             # create order
             create_order = Order(user=user, full_name=full_name, email=email, address=shipping_address, amount_paid=amount_paid)
             create_order.save()

             # create order items

             # get the order od
             order_id = create_order.pk

             # get product info
             for product in cart_products:
                 product_id = product.id

                 if product.is_sale:
                     price = product.sale_price
                 else:
                     price = product.price

                 for key,value in quantities().items():
                     if int(key) == product_id:
                         #create ordr item
                         create_order_item = OrderItem(order=create_order, product=product, user=user, quantity=value, price=price)
                         create_order_item.save()

             # delete cart items
             for key in list(request.session.keys()):
                 if key == "session_key":
                     del request.session["session_key"]               
                
             messages.success(request, "Order Placed!")
             return redirect('/')
        else:
            # guest user
            create_order = Order(full_name=full_name, email=email, address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # create order items

            # get the order od
            order_id = create_order.pk

            # get product info
            for product in cart_products:
                product_id = product.id

                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                for key,value in quantities().items():
                    if int(key) == product_id:
                        #create ordr item
                        create_order_item = OrderItem(order=order_id, product=product_id, quantity=value, price=price)
                        create_order_item.save()

            # delete cart items
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session["session_key"]

            messages.success(request, "Order Placed!")
            return redirect('/')
    else:
        messages.success(request, "Access Denied")
        return redirect('/')

def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants
        totals = cart.cart_total()

        # Create a session with shipping info for later use
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        billing_form = BillingForm()
        if request.user.is_authenticated:
            return render(request, 'payment/billing_info.html', {'cart_products': cart_products, 'quantities':quantities, 'totals':totals, 'shipping_info':request.POST, 'billing_form':billing_form})
        else:
            # guest user
            return render(request, 'payment/billing_info.html', {'cart_products': cart_products, 'quantities':quantities, 'totals':totals, 'shipping_info':request.POST, 'billing_form':billing_form})
    else:
        messages.success(request, "Access Denied")
        return redirect('/')

def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html', {'cart_products': cart_products, 'quantities':quantities, 'totals':totals, 'shipping_form':shipping_form})
    else:
        # guest user
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html', {'cart_products': cart_products, 'quantities':quantities, 'totals':totals, 'shipping_form':shipping_form})

def payment_success(request):
    return render(request, "payment/payment_success.html")
