from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required

from . import views

urlpatterns = [
    # main route
    path('', views.index, name='index'),
    # post related routes
    path('post/detail/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/delete/<slug:slug>/', views.delete_post, name='post_delete'),
    path('post/create/', staff_member_required(views.PostCreate.as_view()), name='post_create'),
    path('post/update/<slug:slug>/', staff_member_required(views.PostUpdate.as_view()), name='post_update'),
    # comments related routes
    path('comment/<str:action>/<int:pk>/', views.activate_comment, name='activate_comment')
]
app_name = 'blog'