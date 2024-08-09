from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('contact/',views.contact,name="contact"),
    path('register/',views.register,name="register"),
    path('login/',views.loginPage,name="login"),
    path('logout/',views.logoutPage,name="logout"),
    path('category/',views.category,name="category"),
    path('product/<str:id>',views.product,name="product"),
    path('product_details/<str:cname>/<str:pname>',views.product_details,name="product_details"),
    path('addCart/',views.addCart,name="addCart"),
    path('cart/',views.cart,name="cart"),
    path('cart_remove/<int:id>',views.cart_remove,name="cart_remove"),
    path('address/',views.address,name="address"),
    path('success/',views.success,name="success"),
    path('order/',views.order,name="order"),
    path('finals/',views.finals,name="finals"),
    path('clear/',views.clear,name="clear"),
]