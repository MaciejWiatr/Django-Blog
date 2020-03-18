from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, FormView, UpdateView
from .forms import CommentForm, PostForm
from .models import Post, Comment


def index(request):
    """
    Main view
    """

    template = 'blog/index.html'
    posts = Post.objects.all()
    query = request.GET.get("q")
    try:
        latest = posts.order_by('-pub_date')[0]
    except:
        latest = ""
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(tags__name__icontains=query) |
            Q(text__icontains=query)
        ).distinct()
    context = {
        'posts': posts,
        'latest': latest
    }
    return render(request, template, context)


# Post related views
def post_detail(request, slug):
    template = 'blog/detail.html'
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, "Twój komentarz został dodany i czeka na zaakceptowanie")
            return redirect("blog:post_detail", slug=slug)
    else:
        form = CommentForm
        accepted_comments = post.comments.filter(active=True).order_by('-created_on')
        not_accepted_comments = post.comments.filter(active=False).order_by('-created_on')
        tags = post.tags.all()
        return render(request, "blog/detail.html",
                      {'post': post, 'comments': accepted_comments, 'not_accepted': not_accepted_comments, 'tags': tags,
                       'form': form})


class PostCreate(FormView):
    template_name = "blog/post_form.html"
    model = Post
    form_class = PostForm
    success_url = '/'
    fields = ['title', 'text', 'image', 'files']

    def form_valid(self, form):
        post = form.save()
        post.save()
        return super().form_valid(form)


class PostUpdate(UpdateView):
    model = Post
    fields = ['title', 'text', 'image', 'files']


@staff_member_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    messages.success(request, f'Post "{post.title[:15]}" id:{post.id} został usunięty')
    post.delete()
    return redirect("blog:index")


# Comments related views

@staff_member_required
def activate_comment(request, action, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment_post = comment.post
    if action == 'activate':
        comment.active = True
        comment.save()
        messages.success(request, 'Komentarz został zaakceptowany')
        return redirect("blog:post_detail", slug=comment_post.slug)
    elif action == 'delete':
        comment.delete()
        messages.warning(request, 'Komentarz został usunięty')
        return redirect("blog:post_detail", slug=comment_post.slug)
