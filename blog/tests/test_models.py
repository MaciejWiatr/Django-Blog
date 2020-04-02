from django.test import TestCase
from blog.models import Post, NewsletterSubscription, Comment
from blog.views import *
from django.urls import resolve
from .utils import clear_files


class TestModels(TestCase):

    def setUp(self):
        self.TestPost = Post.objects.create(
            title='TestPost',
            text='TestPost',
            tags='test,post',
        )

        self.TestComment = Comment.objects.create(
            post=self.TestPost,
            text='TestComment'
        )

        self.TestNewsletterSub = NewsletterSubscription.objects.create(
            email='test_mail@test_mail.com'
        )

    def tearDown(self):
        clear_files()

    def test_post_image_assigned(self):
        self.assertTrue(self.TestPost.image.name)

    def test_post_image_compressed(self):
        pass  # ill add it in the future

    def test_post_slug_assigned(self):
        self.assertTrue(self.TestPost.slug)

    def test_post_get_urls_correct(self):
        urls = {
            'absolute': [self.TestPost.get_absolute_url(), post_detail],
            'delete': [self.TestPost.get_delete_url(), post_delete],
        }

        for _, func_compare in urls.items():
            func_name = resolve(func_compare[0]).func
            self.assertEquals(func_name, func_compare[1])

    def test_post_get_latest(self):
        latest = Post.objects.latest()
        self.assertEquals(latest, self.TestPost)

    def test_post_search(self):
        search = Post.objects.search('Test')
        self.assertEquals(search[0], self.TestPost)

    def test_post_correct_str(self):
        self.assertEquals(self.TestPost.__str__(), self.TestPost.title)

    def test_comment_relation(self):
        self.assertEquals(self.TestComment.post.title, self.TestPost.title)

    def test_comment_default_active(self):
        self.assertEquals(self.TestComment.active, False)

    def test_newsletter_code_assigned(self):
        self.assertTrue(self.TestNewsletterSub.code)

    def test_newsletter_default_active(self):
        self.assertEquals(self.TestNewsletterSub.active, True)
