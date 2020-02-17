from django.urls import path

from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('detail/<int:pk>/', views.detail, name='detail'),
]
app_name = 'blog'
