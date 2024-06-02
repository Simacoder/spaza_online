from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

# Create your views here.

def home(request):
    return render(request, "spaza_app/home.html")

class CategoryView(View):
    def get(self, request):
        return render(request, "spaza_app/category.html")
