from django.test import TestCase
from django.urls import reverse, resolve
from blog.views import *


class TestUrls(TestCase):

    def test_index_url_is_resolved(self):
        url = reverse('blog:index')
        self.assertEquals(resolve(url).func, index)

    def test_post_create_url_resolves(self):
        url = reverse('blog:post_create')
        self.assertEquals(resolve(url).func.view_class, PostCreate)

    def test_post_update_url_resolves(self):
        url = reverse('blog:post_update', args=['test_case'])
        self.assertEquals(resolve(url).func.view_class, PostUpdate)

    def test_post_delete_url_resolves(self):
        url = reverse('blog:post_delete', args=['test_case'])
        self.assertEquals(resolve(url).func, post_delete)
