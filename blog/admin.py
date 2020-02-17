from django.contrib import admin

from .models import Post, Comment


# Register your models here

class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'created_on', 'active')
    list_filter = ('created_on', 'active')
    search_fields = ('text',)
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


admin.site.register(Comment, CommentAdmin)
admin.site.register(Post)
