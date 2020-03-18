from django.db import models


class PostQuerySet(models.QuerySet):

    def get_latest_post(self):
        try:
            latest = self.order_by('-pub_date')[0]
        except:
            latest = []
        return latest


class PostManager(models.Manager):

    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def latest(self):
        return self.get_queryset().get_latest_post()


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
