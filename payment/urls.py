from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('', views.detail, name = 'detail'),
    path('<int:pk>/buy/', views.buy, name = 'buy'),
    path('<int:pk>/confirm/', views.confirm, name = 'confirm'),
    path('/refuse_funds/', views.refuse_funds, name = 'refuse_funds'),
    path('<int:pk>/accept_funds/<int:short_of>/', views.accept_funds, name = 'accept_funds'),
    
]
