
from django.contrib import admin
from django.urls import path
from sales import views
from sales.views import site_home, products_list, customers, orders, order_details, add_to_cart
from accounts.views import login_page, signin, register_page, register,logout_user, dashboard
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", site_home, name="home"),
]

urlpatterns +=[
    path("products", products_list, name="products"),
    path("customers", customers, name="customers"),
    path("orders/<int:cust_id>", orders, name="orders"),
    path("order_details/<int:order_id>", order_details, name="order_details"),
    
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='cart'),
]

urlpatterns += [
    path("login_page", login_page, name="login_page"),
    path("signin", signin, name="signin"),
     path('logout/', logout_user, name='logout'),
    
    path("register_page", register_page, name='register_page'),
    path("register", register, name='register'),
    
    path('dashboard/', dashboard, name='dashboard'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)