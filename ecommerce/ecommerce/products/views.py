from django.shortcuts import render
from .models import Product

# Create your views here.
def products(request):
    return render(request, 'products/products.html', {'Productss': Product.objects.all()})

def product(request):
    return render(request, 'products/product.html',{'Product_c':Product.objects.get(id=1)})

def index(request):
    return render(request, 'products/index.html', {'one_product':Product.objects.all().filter(category='Phone')})