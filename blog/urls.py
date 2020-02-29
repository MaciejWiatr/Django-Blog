from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:pk>/', views.post_detail, name='detail'),
    path('comment/<str:action>/<int:pk>/', views.activate_comment, name='activate_comment')
]
app_name = 'blog'
