from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from item.models import Item
# Create your views here.

@login_required
def index(request):
    new_items = Item.objects.filter(created_by = request.user).filter(is_sold = False)
    sold_items = Item.objects.filter(created_by = request.user).filter(is_sold = True)
    
    return render(request, 'dashboard/index.html', context={
        'new_items': new_items,
        'sold_items': sold_items,
    })
