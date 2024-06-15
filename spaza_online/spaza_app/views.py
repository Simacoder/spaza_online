from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from  django.db.models import Q
from django.conf import settings
import razorpay
from . models import Cart, Customer, Product
from . forms import ContactForm, CustomerProfileForm, CustomerRegistrationForm
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, "spaza_app/home.html")

def about(request):
    return render(request, "spaza_app/about.html")

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Get the form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
    return render(request, "spaza_app/contact.html")


class CategoryView(View):
    def get(self, request, val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, "spaza_app/category.html", locals())

class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request, "spaza_app/category.html", locals())
    
class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, "spaza_app/productdetail.html", locals())
    

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, "spaza_app/customerregistration.html", locals())
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User!  registered succesfully!!!")
        else:
            messages.warning(request, "Invalid input!!!")
        return render(request, "spaza_app/customerregistration.html", locals())
    
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, "spaza_app/profile.html", locals())
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            province = form.cleaned_data['province']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, province=province,zipcode=zipcode)
            reg.save()
            messages.success(request, "Profile save successfully!!")
        else:
            messages.warning(request, "Invalid input")

        return render(request, "spaza_app/profile.html", locals())
    


def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, "spaza_app/address.html", locals())

class updateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, "spaza_app/updateAddress.html", locals())
    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.province = form.cleaned_data['province']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Profile Update successfully!!!")
        else:
            messages.warning(request, "Invalid input!!!")
        return redirect("address")
    
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect("/cart")

def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 60
    return render(request, 'spaza_app/addtocart.html', locals())

class checkout(View):
    def get(self, request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount =famount + 60
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {"amount": razoramount, "currency": "ZAR", "receipt": "order_rcptid_11"}
        payment_response = client.order.create(data = data)
        print(payment_response)
        return render(request, 'spaza_app/checkout.html', locals())


def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        cartOb = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        cartOb.quantity += 1
        cartOb.save()
        user = request.user
        cart = Cart.objects.filter(user = user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount  + value
        totalamount = amount + 60 
        # creating data object
        data = {
            'quantity':cartOb.quantity,
            'amount':amount,
            'totalamount': totalamount


        }
        return JsonResponse(data)
    
def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        cartOb = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        cartOb.quantity -= 1
        cartOb.save()
        user = request.user
        cart = Cart.objects.filter(user = user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 60 
        # creating data object
        data = {
            'quantity':cartOb.quantity,
            'amount':amount,
            'totalamount': totalamount


        }
        return JsonResponse(data)
    
def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        cartOb = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        cartOb.delete()
        user = request.user
        cart = Cart.objects.filter(user = user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 60 
        # creating data object
        data = {
            'amount':amount,
            'totalamount': totalamount


        }
        return JsonResponse(data)
        



