from django.shortcuts import render,get_object_or_404, redirect
from item.models import Item
from .models import Conversation, ConversationMessage
from .forms import ConversationMessageForm
# Create your views here.

def newConversation(request,item_pk):
    item = get_object_or_404(Item, pk = item_pk)
    
    if item.created_by == request.user:
        return redirect('dashboard:index')
    
    conversations = Conversation.objects.filter(item=item).filter(member__in = [request.user.id])
    
    if conversations:
        pass 
    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        
        if form.is_valid():
            conversation = Conversation.objects.create(item = item)
            conversation.member.add(request.user)
            conversation.member.add(item.created_by)
            conversation.save()
            
            conversation_message = form.save(commit=False)
            conversation_message.conversation  = conversation
            conversation_message.created_by = request.user
            conversation_message.save()
            
            return redirect('item:detail', pk = item.pk)
    else:
        form = ConversationMessageForm()
    
    return render(request, 'conversation/new.html', context={
        'form': form,
        })