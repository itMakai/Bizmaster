from django.shortcuts import render
from sales.models import Product, Customer, Order, OrderDetail
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, CartItem
from django.contrib.auth.decorators import login_required

# Create your views here.

def site_home(request):
    return render(request, 'index.html')
    
def products_list(request):
    products = Product.objects.all()
    context = {
        'products': products, 
    }
    return render(request, 'products.html', context)

def customers(request):
    customers = Customer.objects.all()
    context = {'customers': customers}
    return render(request, 'customers.html', context)

def orders(request, cust_id):

    current_customer = Customer.objects.get(id=cust_id)

    if current_customer:
        orders = Order.objects.filter(customer_=cust_id)
        context = {'orders': orders}
        
    context.update({'customer': current_customer})
    return render(request, 'orders.html', context)

def order_details(request, order_id):
    selected_order = Order.objects.get(id=order_id)
    order_details = OrderDetail.objects.filter(order=selected_order)
    
    for detail in order_details:
        detail.amount = detail.quantity * detail.product.price
        
    context = {
        'order': selected_order,
        'order_details': order_details
    }
    return render(request, 'order_details.html', context)


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect('cart')

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    return render(request, 'cart.html', {'cart_items': cart_items})