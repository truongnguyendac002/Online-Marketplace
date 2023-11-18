from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('', views.detail, name = 'detail'),
    path('<int:pk>/buy/', views.buy, name = 'buy'),
    
]
