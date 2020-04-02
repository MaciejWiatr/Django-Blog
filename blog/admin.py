from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from .models import Post, Comment, NewsletterSubscription


def register_models(model_list):
    for model, model_admin in models_list.items():
        try:
            admin.site.register(model, model_admin)
        except AlreadyRegistered:
            pass


class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'created_on', 'active')
    list_filter = ('created_on', 'active')
    search_fields = ('text',)
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'image', 'slug', 'tag_list', 'pub_date')
    search_fields = ('text',)
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('tags',)

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())


class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'active', 'join_date', 'code')
    list_filter = ('join_date', 'active')
    search_fields = ('email',)
    actions = ['disconnect_newsletter', 'join_newsletter']

    def disconnect_newsletter(self, request, queryset):
        queryset.update(active=False)

    def join_newsletter(self, request, queryset):
        queryset.update(active=True)


models_list = {
    Comment: CommentAdmin,
    Post: PostAdmin,
    NewsletterSubscription: NewsletterAdmin
}

# Register your models here
register_models(models_list)
