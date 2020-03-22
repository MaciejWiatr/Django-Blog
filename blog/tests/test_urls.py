from django.test import SimpleTestCase
from django.urls import reverse, resolve
from blog.views import *


class TestUrls(SimpleTestCase):

    def test_index_url_is_resolved(self):
        url = reverse('blog:index')
        self.assertEquals(resolve(url).func, index)
