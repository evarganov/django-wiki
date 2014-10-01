from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client


class WebTestBase(TestCase):
    def setUp(self):
        super(TestCase, self).setUp()
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
        except ImportError:
            from django.contrib.auth.models import User
        User.objects.create_superuser('admin', 'nobody@example.com', 'secret')
        self.c = c = Client()
        c.login(username='admin', password='secret')


class ArticleTestBase(WebTestBase):
    """Base class for web client tests, that sets up initial root article."""
    def setUp(self):
        super(ArticleTestBase, self).setUp()
        response = self.c.post(reverse('wiki:root_create'), {'content': 'root article content', 'title': 'Root Article'}, follow=True)
        self.assertEqual(response.status_code, 200) # sanity check
        self.example_data = {
                'content': 'The modified text',
                'current_revision': '1',
                'preview': '1',
                #'save': '1',  # probably not too important
                'summary': 'why edited',
                'title': 'wiki test'}

    def tearDown(self):
        super(ArticleTestBase, self).tearDown()
        # clear Article cache before the next test
        from wiki.models import Article
        Article.objects.all().delete()

    def get_by_path(self, path):
        """Get the article response for the path.
           Example:  self.get_by_path("Level1/Slug2/").title
        """
        return  self.c.get(reverse('wiki:get', kwargs={'path': path}))
