from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
# Create your views here.

@login_required
def detail(request):
    wallet = Wallet.objects.filter(user=request.user).first()
    if wallet is None:
        wallet = Wallet.objects.create(user=request.user)
    
    
    
    return render(request, 'payment/index.html', context={
        'wallet':wallet,
        
    })   

@login_required
def buy(request, pk):
    return render(request, 'payment/index.html')