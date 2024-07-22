from django.shortcuts import redirect, render
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from sales.models import Customer
from django.shortcuts import render
from .models import Profile, Order, Favorite
from django.contrib.auth.decorators import login_required


# Create your views here.
def login_page(request):
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('login_page') 

def signin(request):
    username =request.POST.get("inputUsername")
    password =request.POST.get("inputPassword")

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return render(request, 'index.html')
    else:
        context = {'message': 'Login failed. Username or password incorrect. Please try again.'}
        return render(request, 'login.html', context)
    
def register_page(request):
        return render(request, 'register.html')
    
def register(request):
        username = request.POST["inputUsername"]
        password1 = request.POST["inputPassword1"]
        password2 = request.POST["inputPassword2"]
        email = request.POST["inputEmail"]
        first_name = request.POST["inputFirstname"]
        last_name =request.POST["inputLastname"]
        phone =request.POST["inputPhone"]
        
        context = {
            'username' : username,
            'email' :email,
            'first_name' :first_name,
            'last_name' : last_name,
        }
        
        if password1 != password2:
            context.update(
                {
                    'error_message': 'Passwards must match. please try again'
                }
            )
            return render(request, 'register.html', context)
        
        if User.objects.filter(username=username).exists():
            context.update(
                {
                    'error_message': 'username exists'
                }
            )
            return render (request, 'register.html', context)
        
        user = User.objects.create_user(username=username, email=email, password=password1, first_name =first_name, last_name =last_name)
        user.save()
        customer = Customer.objects.create(first_name =first_name, last_name =last_name, email=email, user=user)
        customer.save()
        
        return render (request, 'login.html', context)
        
        
@login_required
def dashboard(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None
        error_message = "Please complete your profile."  

    recent_orders = Order.objects.filter(user=user).order_by('-date')[:5]
    favorites = Favorite.objects.filter(user=user)
    
    context = {
        'user': user,
        'profile': profile,
        'recent_orders': recent_orders,
        'favorites': favorites,
    }

    if profile is None:
        context['error_message'] = error_message

    return render(request, 'dashboard.html', context)


        
        
        
        
 
