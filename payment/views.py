from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import *
# Create your views here.

@login_required
def detail(request):
    user = request.user
    wallet = Wallet.objects.filter(user=request.user).first()
    if wallet is None:
        wallet = Wallet.objects.create(user=request.user)
    
    transactions = Transaction.objects.filter(Q(buyer=user) | Q(seller=user)).all()
    
    return render(request, 'payment/index.html', context={
        'wallet':wallet,
        'transactions':transactions,
    })   

@login_required
def buy(request, pk):
    item = Item.objects.get(pk=pk)
    wallet = Wallet.objects.get(user = request.user)
    short_of = item.price - wallet.balance
    if wallet.balance >= item.price:
        transaction = Transaction.objects.create(
            buyer = request.user,
            item = item,
            seller = item.created_by,
        )
        
        return redirect( 'payment:detail')
    else:
        message = "You're short of "+ str(short_of) +"$ to purchase this item !\nWant to add "+ str(short_of) +" $ into your wallet ?"
        return render(request, 'payment/confirm.html', context={
        'wallet' : wallet,
        'message': message,
        'short_of': int(short_of) + (short_of > int(short_of))
    })

@login_required
def accept_funds(request,pk, short_of):
    wallet = Wallet.objects.get(pk=pk)
    wallet.balance += short_of
    wallet.save()
    
    return redirect( 'payment:detail')

@login_required
def refuse_funds(request):    
    return redirect( 'payment:detail')

@login_required
def confirm(request,pk):
    wallet = Wallet.objects.get(pk=pk)
    return render(request, 'payment/confirm.html', context={
        'wallet' : wallet,
        'message': 'Add 100 $ into your wallet ?',
        'short_of': 100
    })