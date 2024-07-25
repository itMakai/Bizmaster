from django.shortcuts import render
from sales.models import Product, Customer, Order, OrderDetail, Category
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, CartItem
from django.contrib.auth.decorators import login_required 
from django.shortcuts import render, get_object_or_404

# Create your views here.

def site_home(request):
    categories = Category.objects.all()
    return render(request, 'index.html', {'categories': categories})
    
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


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart

    return redirect('cart')

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        total += product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total': product.price * quantity,
        })

    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'cart.html', context)

@login_required
def checkout(request):
    
    return render(request, 'checkout.html')





def category_list(request):
    categories = Category.objects.filter(parent_category__isnull=True)
    return render(request, 'categories/category_list.html', {'categories': categories})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    subcategories = category.subcategories.all()
    products = Product.objects.filter(category=category)
    return render(request, 'categories/category_details.html', {'category': category, 'subcategories': subcategories, 'products': products})
