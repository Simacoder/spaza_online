from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from . models import Product
from . forms import CustomerRegistrationForm

# Create your views here.

def home(request):
    return render(request, "spaza_app/home.html")

def about(request):
    return render(request, "spaza_app/about.html")

def contact(request):
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



