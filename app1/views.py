from django.shortcuts import render, redirect
from .import models
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    data=models.Product.objects.filter(trending=1,status=0)
    cart=models.Cart.objects.filter(user=request.user)
    count=len(cart)
    return render(request,"home.html",{"data":data,"cartCount":count})

def about(request):
    return render(request,"about.html")

@login_required(login_url="login")
def contact(request):
    if request.method=='POST':
        name=request.POST["name"]
        email=request.POST["email"]
        mobile=request.POST["mobile"]
        time=request.POST["time"]

        cons=models.Support.objects.create(name=name,mail=email,mobile=mobile,time=time)
        cons.save()
        messages.success(request,f"Our Support Will Contact You In {time}")
        return redirect("home")
    return render(request,"contact.html")

def register(request):
    if request.method=='POST':
        fname=request.POST["fname"]
        lname=request.POST["lname"]
        email=request.POST["mail"]
        username=email
        pwd1=request.POST["pwd1"]
        pwd2=request.POST["pwd2"]

        if pwd1==pwd2:
            if models.User.objects.filter(email=email).exists():
                messages.warning(request,"E-mail Already Exists...!")
                return redirect("register")
            elif not email.endswith("@gmail.com"):
                messages.warning(request,"Use only Gmail Account..!")
                return redirect("register")
            else:
                user=models.User.objects.create_user(username=username,email=email,password=pwd1,first_name=fname,last_name=lname)
                user.save()
                messages.success(request,f"{fname}, Now Your Are Login..")
                return redirect("login")
        else:
            messages.warning(request,"Password does not match..!")
            return redirect("register")
    else:
        return render(request,"register.html")

def loginPage(request):
    if not request.user.is_authenticated:
        if request.method=='POST':
            email=request.POST["mail"]
            pwd=request.POST["pwd"]
            user=authenticate(username=email,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,f"Welcome {request.user.first_name}..")
                return redirect("home")
            else:
                messages.warning(request,"Please Check Your Email or Password...!")
                return redirect("login")
        else:
            return render(request,"login.html")
    else:
        return redirect("home")

def logoutPage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.warning(request,"Please login..!")
        return redirect("login")
    else:
        return redirect("home")


def category(request):
    cats=models.Category.objects.filter(status=False)
    return render(request,"category.html",{'cats':cats})

def product(request,id):
    if models.Category.objects.filter(id=id):
        data=models.Category.objects.get(id=id)
        prod=models.Product.objects.filter(category__id=id)
        return render(request,"product.html",{"products":prod,"cat":id,"data":data})
    else:
        messages.warning(request,"Product Not Available...!")
        return redirect("home")
    
def product_details(request,cname,pname):
    if models.Category.objects.filter(id=cname,status=0):
        if models.Product.objects.filter(id=pname,status=0):
            details=models.Product.objects.get(id=pname)
            return render(request,"pro_details.html",{'details':details})
        else:
            messages.warning(request,"Product Not Available...!")
            return redirect("home")
    else:
        messages.warning(request,"Category Not Available...!")
        return redirect("home")

def addCart(request):
    if request.method=='POST':
        id=request.POST["pro_id"]
        quantity=int(request.POST["pro_qty"])

        product=models.Product.objects.get(id=id)

        if product:
            if models.Cart.objects.filter(user=request.user.id,product_id=id):
                cart=models.Cart.objects.get(user=request.user.id, product_id=id)
                cart.product_qty +=1
                cart.save()
                messages.success(request,"Item Added In Cart..")
                return redirect("cart")
            else:
                if product.quantity > quantity:
                    models.Cart.objects.create(user=request.user,product_id=id,product_qty=quantity)
                    messages.success(request,"Item Added In Cart..")
                    return redirect("cart")
                else:
                    messages.warning(request,"Item Not Avaiable..!")
                    return redirect("home")
        else:
            messages.warning(request,"Product Not Available...!")
            return redirect("home")
        
def cart(request):
    data=models.Cart.objects.filter(user=request.user)
    adds=models.Address.objects.filter(user=request.user)
    sum=0
    for datas in data:
        sum+=datas.total_price

    return render(request,"cart.html",{'data':data,'adds':adds,"sum":sum})

def cart_remove(request,id):
    cart=models.Cart.objects.get(id=id)
    cart.delete()
    messages.warning(request,"Item has deleted..!")
    return redirect('cart')


def success(request):
    if request.method=='POST':
        value=request.POST['address']
        carts=request.POST['cart']
        print(value)
        print(carts)
        
        name=request.POST["name"]
        amt=int(request.POST["amt"])*100
        client=razorpay.Client(auth=("rzp_test_wWHPuNDhC1ivkp","FCNjFqzGy2DG2trsKvuHr8wI"))
        data = { "amount": amt, "currency": "INR", "receipt": "order_rcptid_11" }
        payment = client.order.create(data=data)
        print(payment)
        base=Payment(user=request.user,name=name,amount=amt,payment_id=payment['id'])
        base.save()
        

        order=models.Order.objects.create(user=request.user,address_id=value,cart_id=carts)
        order.save()

        return render(request,"payment.html",{'payment':payment})
    
from django.views.decorators.csrf import csrf_exempt
from .models import Payment
import razorpay


def pay(request):
    if request.method=='POST':
        name=request.POST["name"]
        amt=int(request.POST["amt"])*100
        client=razorpay.Client(auth=("rzp_test_wWHPuNDhC1ivkp","FCNjFqzGy2DG2trsKvuHr8wI"))
        data = { "amount": amt, "currency": "INR", "receipt": "order_rcptid_11" }
        payment = client.order.create(data=data)
        print(payment)
        base=Payment(user=request.user,name=name,amount=amt,payment_id=payment['id'])
        base.save()
        return render(request,"index.html",{'payment':payment})
    return render(request,"index.html")

@csrf_exempt
def finals(request):
    return redirect("order")

def clear(request):
    dele=models.Cart.objects.filter(user=request.user)
    dele.delete()
    messages.success(request,"Order Confirmed..!")
    return redirect("home")

def order(request):
    order=models.Order.objects.filter(user=request.user)
    delevery=models.Delivery.objects.create(
        user=request.user,
        cat_name=order[0].cart.product.category.name,
        products=order[0].cart.product.name,
        pro_qty=order[0].cart.product_qty,
        total_amt=order[0].cart.total_price,
        total_price=order[0].address.mobile,
        hno=order[0].address.house_no,
        street=order[0].address.street,
        area=order[0].address.area,
        city=order[0].address.city,
        pincode=order[0].address.pincode
    )
    delevery.save()
    return redirect("clear")

def address(request):
    if request.method=='POST':
        mobile=request.POST["mob"]
        house_no=request.POST["house"]
        street=request.POST["street"]
        area=request.POST["area"]
        city=request.POST["city"]
        pincode=request.POST["pin"]

        if models.Address.objects.filter(user=request.user,house_no=house_no,street=street).exists():
            messages.warning(request,"Address already exists..!")
            return redirect('address')
        else:
            data=models.Address.objects.create(user=request.user,mobile=mobile,house_no=house_no,street=street,area=area,city=city,pincode=pincode)
            data.save()
            messages.success(request,"Address Successfully Added..")
            return redirect("cart")
    else:
        return render(request,"address.html")