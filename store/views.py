from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignUpForm, UserUpdateForm, ChangePasswordForm, UserInforForm

from payment.forms import ShippingForm
from payment.models import ShippingAddress

from django.db.models import Q
import json
from cart.cart import Cart


def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))

        if not searched:
             messages.success(request, ("The product you searched doesn't exist. Please try again...."))
             return render(request, 'search.html', {})
        else:
            return render(request, 'search.html', {'searched':searched})
    else:
        return render(request, 'search.html', {})

def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)

        form = UserInforForm(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()

            messages.success(request, ("User info have been updated successfully."))
            return redirect('/')
        return render(request, 'update_info.html', {'form':form, 'shipping_form':shipping_form})
    else:
        messages.success(request, ("You must be logged in to access this page."))
        return redirect('/')

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

def about(request):
    return render(request, 'about.html')

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user

        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, ("Your password have been updated successfully.."))
                # Login back cause dj logs out user once password changed
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form':form})
    else:
        messages.success(request, ("You must be logged in to access this page."))
        return redirect('/')

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        # current_user = request.user
        user_form = UserUpdateForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, ("User profile have been updated successfully."))
            return redirect('/')
        return render(request, 'update_user.html', {'user_form':user_form})
    else:
        messages.success(request, ("You must be logged in to access this page."))
        return redirect('/')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # do some shopping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart
            # check for empty cart
            if saved_cart:
                converted_cart = json.loads(saved_cart)
            else:
                converted_cart = {}
                
            cart = Cart(request)

            for key, value in converted_cart.items():
                cart.add(product=key, quantity=value)

            messages.success(request, ("You have been logged in!."))
            return redirect('/')
        else:
            messages.success(request, ("Username or password is incorrect."))
            return redirect('login')
    else:    
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out."))
    return redirect('/')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have registered successfully! Please fill the user info below.."))
            return redirect('update_info')
        else:
           messages.success(request, ("Oops! Something went wrong. Please fill the form again."))
           return redirect('register') 
    else:
        return render(request, 'register.html', {'form':form})


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})


def category(request, name):
    name = name.replace('-', ' ')

    try:
        category = Category.objects.get(name=name)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'category':category, 'products':products})
    except:
        messages.success(request, ("That category doesn't exist."))
        return redirect('register')
    


def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories':categories})

    
    

