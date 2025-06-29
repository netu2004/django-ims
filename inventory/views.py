# inventory/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import UserRegisterForm, ProductForm, OrderForm
from .models import Product, Order
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth import logout



def home(request):
    return render(request, 'inventory/home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'inventory/register.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.is_superuser:
        users = User.objects.count()
        products = Product.objects.count()
        orders = Order.objects.count()
        return render(request, 'inventory/admin_dashboard.html', {
            'users': users, 'products': products, 'orders': orders
        })
    else:
        user_orders = Order.objects.filter(created_by=request.user)  # ✅ FIXED
        return render(request, 'inventory/user_dashboard.html', {'orders': user_orders})

@login_required
def product_list(request):
    if request.user.is_superuser:
        products = Product.objects.all()
        return render(request, 'inventory/product_list.html', {'products': products})
    return redirect('dashboard')

@login_required
def product_add(request):
    if request.user.is_superuser:
        form = ProductForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('product_list')
        return render(request, 'inventory/product_form.html', {'form': form})
    return redirect('dashboard')

@login_required
def create_order(request):
    form = OrderForm(request.POST or None)
    if form.is_valid():
        order = form.save(commit=False)
        order.created_by = request.user  # ✅ FIXED
        order.save()
        return redirect('dashboard')
    return render(request, 'inventory/order_form.html', {'form': form})