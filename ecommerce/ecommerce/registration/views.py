from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import User

# Create your views here.
# def login(request):
#     return render(request, 'registration/login.html')

# def register(request):
#     username = request.POST.get('username')
#     password = request.POST.get('password1')
#     email = request.POST.get('email')
#     user_data = User(username=username, password=password, email=email)
#     user_data.save()
#     return render(request, 'registration/register.html')



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
