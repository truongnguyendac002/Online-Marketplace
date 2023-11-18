from django.shortcuts import render, redirect
from django.contrib.auth import logout
from item.models import *
from .forms import SignupForm
from payment.models import Wallet
# Create your views here.

def index(request):
    items = Item.objects.filter(is_sold = False)[0:6]
    category = Category.objects.all()
    
    return render(request, 'core/index.html', {
        'categories' : category,
        'items' : items,
        
    })

def contact(request):
    return render(request, 'core/contact.html')

def logout_view(request):
    logout(request)
    
    return redirect('core:index')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        print(form.data)  
        if form.is_valid():
            user = form.save()
            Wallet.objects.create(user=user)
            
            return redirect('/login/')
    else:
        form = SignupForm()
    return render(request, 'core/signup.html', {
        'form': form,
    })