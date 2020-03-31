from django.test import TestCase, Client
from django.urls import reverse
from blog.urls import *
from blog.views import *
from blog.models import *
from django.contrib.auth.models import User


class ViewsMixin(object):

    def get_response(self, url, method):
        # client = Client()
        if method == 'GET':
            resp = self.client.get(reverse(url[0], args=url[1]))
        elif method == 'POST':
            resp = self.client.post(reverse(url[0], args=url[1]))
        else:
            resp = ''
        return resp

    def is_callable(self, url, user=None, post=None, fail=None, accept_redir=None):
        if user:
            self.client.force_login(user, backend=None)
        if post:
            method = 'POST'
        else:
            method = 'GET'
        if fail:
            resp = self.get_response(url, method=method)
            status = resp.status_code in [404, 302]
            self.assertTrue(status)
        else:
            resp = self.get_response(url, method=method)
            if accept_redir:
                print(resp.status_code)
                status = resp.status_code in [200, 302]
                print(status)
                self.assertTrue(status)
            else:
                self.assertEquals(resp.status_code, 200)


class TestViews(ViewsMixin, TestCase):

    def setUp(self):
        self.client = Client()
        post_args = ['test_case']
        self.urls = {
            'index': ['blog:index', []],
            'post_create': ['blog:post_create', []],
            'post_detail': ['blog:post_detail', ['test_case']],
            'post_update': ['blog:post_update', ['test_case']],
            'post_delete': ['blog:post_delete', ['test_case']]
        }
        self.admin = User.objects.create_superuser(
            username='test_admin',
            email='test@admin.com',
            password='test_admin'
        )
        self.admin.save()
        self.test_post = Post.objects.create(
            title='test_case',
            text='test_case',
            slug='test_case',
            tags='test,case'
        )

    def test_index(self):
        self.is_callable(url=self.urls['index'])
        self.is_callable(url=self.urls['index'], post=True, accept_redir=True)

    def test_post_create_callable_authorized(self):
        # Test authorized get and post request
        self.is_callable(url=self.urls['post_create'], user=self.admin)
        self.is_callable(url=self.urls['post_create'], user=self.admin, post=True)

    def test_post_create_callable_unauthorized(self):
        # Test unauthorized get and post request
        self.is_callable(url=self.urls['post_create'], user=None, fail=True)
        self.is_callable(url=self.urls['post_create'], user=None, post=True, fail=True)

    def test_post_detail_callable(self):
        self.is_callable(url=self.urls['post_detail'])

    def test_post_update_callable_authorized(self):
        # Test authorized get and post request
        self.is_callable(url=self.urls['post_update'], user=self.admin)
        self.is_callable(url=self.urls['post_update'], user=self.admin, post=True)

    def test_post_update_callable_unauthorized(self):
        # Test unauthorized get and post request
        self.is_callable(url=self.urls['post_update'], user=None, fail=True)
        self.is_callable(url=self.urls['post_update'], user=None, post=True, fail=True)

    def test_post_delete_callable_authorized(self):
        # Test authorized get and post request
        self.is_callable(url=self.urls['post_delete'], user=self.admin, accept_redir=True)

    def test_post_delete_callable_authorized_POST(self):
        self.is_callable(url=self.urls['post_delete'], user=self.admin, post=True, accept_redir=True)

    def test_post_delete_callable_unauthorized(self):
        # Test unauthorized get and post request
        self.is_callable(url=self.urls['post_delete'], user=None, fail=True)
        self.is_callable(url=self.urls['post_delete'], user=None, post=True, fail=True)
