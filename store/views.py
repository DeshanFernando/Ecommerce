from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignUpForm, UserUpdateForm


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

def about(request):
    return render(request, 'about.html')

def update_password(request):
    pass

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
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


    return render(request, 'update_user.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
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
            messages.success(request, ("You have registered successfully! Welcome!"))
            return redirect('/')
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

    
    

