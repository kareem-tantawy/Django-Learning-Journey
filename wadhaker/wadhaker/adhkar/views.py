from django.shortcuts import render

# Create your views here.
def morningAdhkar(request):
    return render(request, 'Adhkar/morning_adhkar.html')

def eveningAdhkar(request):
    return render(request, 'Adhkar/evening_adhkar.html')