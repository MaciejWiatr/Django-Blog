from django.db import models
from django.db.models import Q


class PostQuerySet(models.QuerySet):

    def get_latest_post(self):
        try:
            latest = self.order_by('-pub_date')[0]
        except:
            latest = []
        return latest

    def search(self, query):
        return self.filter(
            Q(title__icontains=query) |
            Q(tags__name__icontains=query) |
            Q(text__icontains=query)
        ).distinct()


class PostManager(models.Manager):

    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def latest(self):
        return self.get_queryset().get_latest_post()

    def search(self, query):
        return self.get_queryset().search(query=query)


class CommentQuerySet(models.QuerySet):

    def get_accepted_comments(self):
        return self.filter(active=True).order_by('-created_on')

    def get_not_accepted_comments(self):
        return self.filter(active=False).order_by('-created_on')


class CommentManager(models.Manager):

    def get_queryset(self):
        return CommentQuerySet(self.model, using=self._db)

    def accepted(self):
        return self.get_queryset().get_accepted_comments()

    def not_accepted(self):
        return self.get_queryset().get_not_accepted_comments()


class NewsletterQuerySet(models.QuerySet):

    def get_email_list(self):
        for obj in self.filter(active=True).order_by('-join_date'):
            yield obj.email


class NewsletterManager(models.Manager):

    def get_queryset(self):
        return NewsletterQuerySet(self.model, using=self._db)

    def email_list(self):
        return self.get_queryset().get_email_list()
