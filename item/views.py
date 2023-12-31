from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import NewItemForm, EditItemForm
# Create your views here.

def items(request):
    query = request.GET.get('query','')
    category_id = request.GET.get('category_id',0)
    categories = Category.objects.all()
    
    items = Item.objects.filter(is_sold = False)
    if category_id != 0:
        items = items.filter(category_id = category_id) 
    if query:
        items = items.filter(Q(name__icontains = query) | Q(description__icontains = query))
    
    return render(request, 'item/items.html', context= {
        'items': items,
        'query' : query,
        'categories' : categories,
        'category_id' : int(category_id),
    })

def detail(request,pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category = item.category, is_sold = False).exclude(pk=pk)[0:3]
    is_in_wishlist = False
    
    if request.user.is_authenticated :
        wishlist, created = Wishlist.objects.get_or_create(created_by=request.user)
        is_in_wishlist = wishlist.items.filter(pk=pk).exists()
    
    return render(request, 'item/detail.html', context= {
        'item': item,
        'related_items': related_items,
        'is_in_wishlist': is_in_wishlist,
    })
    
@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            
            return redirect('item:detail', pk = item.id)
    else:
        form = NewItemForm()
    
    return render(request, 'item/form.html', {
        'form':form,
        'title': 'New item'
    })
    
@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by = request.user)
    item.delete()
    
    return redirect('dashboard:index', )

@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by = request.user)
    
    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            
            return redirect('item:detail', pk = item.id)
    else:
        form = EditItemForm(instance=item)
    
    return render(request, 'item/form.html', {
        'form':form,
        'title': 'Edit item'
    })
    
    
@login_required
def wishlist(request):
    wishlist, created = Wishlist.objects.get_or_create(created_by=request.user)
    
    items = wishlist.items.all().filter(is_sold = False)
    wishlist.items.set(items)
    
    return render(request, 'item/wishlist.html', {
        'items': items
    })

    
@login_required
def add_to_wishlist(request, pk):
    item = Item.objects.get(pk = pk)
    wishlist, created = Wishlist.objects.get_or_create(created_by=request.user)
    
    if item not in wishlist.items.all():
        wishlist.items.add(item)
    items = wishlist.items.all()
    
    return render(request,'item/wishlist.html',context={
        'items':items
    })
    
@login_required
def delete_from_wishlist(request, pk):
    item = Item.objects.get(pk = pk)
    wishlist, created = Wishlist.objects.get_or_create(created_by=request.user)
    
    if item in wishlist.items.all():
        wishlist.items.remove(item)
    items = wishlist.items.all()
    
    return render(request,'item/wishlist.html',context={
        'items':items
    })
    