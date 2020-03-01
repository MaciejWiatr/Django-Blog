from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/detail/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/delete/<slug:slug>/', views.delete_post, name='post_delete'),
    path('comment/<str:action>/<int:pk>/', views.activate_comment, name='activate_comment')
]
app_name = 'blog'
