from django.contrib import messages
from django.shortcuts import redirect, render
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from sales.models import Customer
from django.shortcuts import render
from .models import Profile, Order, Favorite
from django.contrib.auth.decorators import login_required
from sales.models import Category

# Create your views here.
def login_page(request):
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('login_page') 


def signin(request):
    if request.method == 'POST':
        username = request.POST.get("inputUsername")
        password = request.POST.get("inputPassword")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to a success page.
        else:
            context = {'message': 'Login failed. Username or password incorrect. Please try again.'}
            return render(request, 'login.html', context)
    
    return render(request, 'login.html')
    
def register_page(request):
        return render(request, 'register.html')
    


def register(request):
    if request.method == 'POST':
        username = request.POST.get("inputUsername")
        password1 = request.POST.get("inputPassword1")
        password2 = request.POST.get("inputPassword2")
        email = request.POST.get("inputEmail")
        first_name = request.POST.get("inputFirstname")
        last_name = request.POST.get("inputLastname")
        phone = request.POST.get("inputPhone")
        
        context = {
            'username': username,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
        }
        
        if password1 != password2:
            context.update({'error_message': 'Passwords must match. Please try again.'})
            return render(request, 'register.html', context)
        
        if User.objects.filter(username=username).exists():
            context.update({'error_message': 'Username already exists.'})
            return render(request, 'register.html', context)
        
        user = User.objects.create_user(username=username, email=email, password=password1, first_name=first_name, last_name=last_name)
        user.save()
        customer = Customer.objects.create(first_name=first_name, last_name=last_name, email=email, user=user)
        customer.save()
        
        messages.success(request, 'Registration successful. Please log in.')
        return redirect('login')
    
    return render(request, 'register.html')
        
        
@login_required
def dashboard(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None
        error_message = "Please complete your profile."  

    recent_orders = Order.objects.filter(user=user).order_by('-date')[:5]
    favorites = Favorite.objects.filter(user=user)
    categories = Category.objects.all()  # Query all categories

    context = {
        'user': user,
        'profile': profile,
        'recent_orders': recent_orders,
        'favorites': favorites,
        'categories': categories,  # Add categories to the context
    }

    if profile is None:
        context['error_message'] = error_message

    return render(request, 'dashboard.html', context)

        
        
        
        
 
