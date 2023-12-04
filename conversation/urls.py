from django.urls import path
from . import  views

app_name = 'conversation'

urlpatterns = [
    path('new/<int:item_pk>/', views.newConversation, name = 'new'),
    path('', views.inbox, name="inbox"),
    path('<int:conversation_pk>/', views.detail, name="detail"),
    
]
