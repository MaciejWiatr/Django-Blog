from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import FormView, UpdateView
from .forms import CommentForm, PostForm, NewsletterForm
from .models import Post, Comment, NewsletterSubscription
from .utils import send_newsletter_confirmation, send_post_notification


# import logging
#
# logger = logging.getLogger(__name__)


def index(request):
    """
    Main view
    """
    if request.method == 'POST':
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            newsletter = newsletter_form.save()
            newsletter.save()
            messages.success(request, 'Twój email został zarejestrowany do newslettera! :)')
            send_newsletter_confirmation(Subscription=newsletter, site_url=request.build_absolute_uri())
            return redirect('blog:index')
        else:
            messages.error(request, 'Ten email już został zarejestrowany')
            return redirect('blog:index')
    else:
        newsletter_form = NewsletterForm
        template = 'blog/index.html'
        posts = Post.objects.all()
        query = request.GET.get("q")
        latest = Post.objects.latest()
        if query:
            posts = posts.search(query)
        context = {
            'posts': posts,
            'latest': latest,
            'query': query,
            'form': newsletter_form,
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
        accepted_comments = post.comments.accepted()
        not_accepted_comments = post.comments.not_accepted()
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
        send_post_notification(post, self.request.build_absolute_uri(), NewsletterSubscription.objects.email_list())
        return super().form_valid(form)


class PostUpdate(UpdateView):
    model = Post
    fields = ['title', 'text', 'image', 'files']


@staff_member_required
def post_delete(request, slug):
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


# Newsletter views
def newsletter_unsub(request, code):
    newsletter = get_object_or_404(NewsletterSubscription, code=code)
    email = newsletter.email
    newsletter.delete()
    return HttpResponse(f'Pomyślnie opuściłeś mój newsletter :( kolego {email}')
