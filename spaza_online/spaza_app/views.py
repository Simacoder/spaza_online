from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from . models import Product

# Create your views here.

def home(request):
    return render(request, "spaza_app/home.html")

class CategoryView(View):
    def get(self, request, val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, "spaza_app/category.html", locals())

