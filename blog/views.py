from django.shortcuts import render

from .models import Post


# Create your views here.

def index(request):
    template = 'blog/index.html'
    posts = Post.objects.all()

    return render(request, template, {'posts': posts})


def detail(request, pk):
    template = 'blog/detail.html'
    post = Post.objects.get(id=pk)
    comments = post.comments.filter(active=True)
    return render(request, "blog/detail.html", {'post': post, 'comments': comments})
