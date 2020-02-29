from django.shortcuts import render, get_object_or_404, redirect

from .forms import CommentForm
from .models import Post, Comment


# Create your views here.

def index(request):
    template = 'blog/index.html'
    posts = Post.objects.all()
    return render(request, template, {'posts': posts})


def post_detail(request, pk):
    template = 'blog/detail.html'
    post = get_object_or_404(Post, id=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect("blog:detail", pk=pk)
    else:
        form = CommentForm
        accepted_comments = post.comments.filter(active=True).order_by('-created_on')
        not_accepted_comments = post.comments.filter(active=False).order_by('-created_on')
        return render(request, "blog/detail.html",
                      {'post': post, 'comments': accepted_comments, 'not_accepted': not_accepted_comments,
                       'form': form})


def activate_comment(request, action, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment_post = comment.post.id
    if action == 'activate':
        comment.active = True
        comment.save()
        return redirect("blog:detail", pk=comment_post)
    elif action == 'delete':
        comment.delete()
        return redirect("blog:detail", pk=comment_post)
