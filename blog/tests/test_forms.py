from django.test import TestCase
from blog.forms import PostForm, NewsletterForm, CommentForm
from blog.models import Post
from blog.tests.utils import clear_files


class TestPostForms(TestCase):

    def setUp(self) -> None:
        self.form = PostForm

    def tearDown(self):
        clear_files()

    def test_post_form_valid_data(self):
        data = {
            'title': 'test_title',
            'tags': 'test,tags',
            'text': 'test_text'
        }
        self.assertTrue(self.form(data=data).is_valid())

    def test_post_form_invalid_data(self):
        data = {
            'invalid': 'data'
        }
        self.assertFalse(self.form(data=data).is_valid())

    def test_post_form_no_data(self):
        data = {}
        self.assertFalse(self.form(data=data).is_valid())

    def test_post_form_clean_slug(self):
        TestPost = Post.objects.create(
            title='TestPost',
            text='TestPost',
            tags='test,post',
        )
        TestPost.save()
        data = {
            'title': 'TestPost',
            'tags': 'TestPost',
            'text': 'test,post'
        }
        self.assertFalse(self.form(data=data).is_valid())


class TestCommentForms(TestCase):
    def setUp(self) -> None:
        self.form = CommentForm

    def test_comment_form_valid_data(self):
        data = {
            'text': 'TestComment'
        }
        self.assertTrue(self.form(data=data).is_valid())

    def test_comment_form_invalid_data(self):
        data = {
            'invalid': 'data'
        }
        self.assertFalse(self.form(data=data).is_valid())

    def test_comment_form_no_data(self):
        data = {
        }
        self.assertFalse(self.form(data=data).is_valid())


class TestNewsletterForms(TestCase):
    def setUp(self) -> None:
        self.form = NewsletterForm

    def test_nwslttr_form_valid_data(self):
        data = {
            'email': 'testmail@testmail.com'
        }
        self.assertTrue(self.form(data=data).is_valid())

    def test_nwslttr_form_invalid_data(self):
        data = {
            'email': 'TotallyNotAnEmail'
        }
        self.assertFalse(self.form(data=data).is_valid())

    def test_nwslttr_no_data(self):
        data = {
        }
        self.assertFalse(self.form(data=data).is_valid())
