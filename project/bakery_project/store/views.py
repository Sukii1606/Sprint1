from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import connection
from django.db.utils import OperationalError
from .models import User
from django.contrib import messages
from django.db.models import Q

def register_view(request):
    if request.method == 'POST':
        username = request.POST['full_name']
        email = request.POST['email']
        password = request.POST['password']

        print('username: ', username)
        print('email: ', email)
        print('password: ', password)

        if User.objects.filter(Q(email=email) | Q(username=username)).exists():
            messages.error(request, "Username or email already taken.")
        else:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                    [username, email, password]
                )
            messages.success(request, "Registered successfully.")
            return redirect('login')
    return render(request, 'store/register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.raw(
            "SELECT * FROM users WHERE email = %s AND password = %s", [email, password]
        )
        if list(user):
            request.session['user_email'] = email
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password.")
    return render(request, 'store/login.html')

def check_database_connection():
    try:
        connection.cursor()
        print("✅ Database connection successful!")
        return True
    except OperationalError as e:
        print("❌ Database connection failed:", e)
        return False
    
def home_view(request):
    return render(request,'store/front.html')


def user_logout(request):
    logout(request)
    return redirect('login')

def cart_view(request):
    return render(request, 'store/cart.html')

def cart_view(request):
    cart_items = [
    ]
    total_price = sum(item['quantity'] * item['price'] for item in cart_items)
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total_price})

from django.shortcuts import render
from .models import Product

def categories(request):
    products = Product.objects.all()
    return render(request, 'store/categories.html', {'products': products})
