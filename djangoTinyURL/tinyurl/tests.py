from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import MyUrl
from .hash import get_tiny_url


class MyUrlTests(TestCase):

    def test_MyUrl_string_is_tiny_url(self):
        """
        MyUrl string is tiny url
        :return:
        """
        my_url = MyUrl(tiny_url='text')
        self.assertIs(f"{my_url}", my_url.original_url)


def create_tiny_url(original_url, num_of_uses=0):
    """
    Create a MyUrl with the given 'tiny_url_text' and 'num_of_uses'
    :param original_url: original url
    :param num_of_uses: the number of times the tiny url was used
    :return: created MyUrl
    """
    return MyUrl.objects.create(original_url=original_url, tiny_url=get_tiny_url(original_url),
                                pub_date=timezone.now(), last_us_date=timezone.now(), num_of_uses=num_of_uses)


class IndexViewTest(TestCase):

    def test_no_tiny_urls(self):
        """
        If no tiny urls exists, an appropriate message is displayed.
        """
        response = self.client.get(reverse('tinyurl:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No tiny url has been added.')
        self.assertQuerysetEqual(response.context['most_frequently_used'], [])

    def test_one_tiny_urls(self):
        """
        Tiny url are displayed on the index page.
        """
        create_tiny_url(original_url='test_url')
        response = self.client.get(reverse('tinyurl:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['most_frequently_used'],
            ['<MyUrl: test_url>']
        )

    def test_two_tiny_urls(self):
        """
        The index page may displayed multiple tiny urls.
        """
        create_tiny_url(original_url='test_url_1', num_of_uses=1)
        create_tiny_url(original_url='test_url_2', num_of_uses=10)
        response = self.client.get(reverse('tinyurl:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['most_frequently_used'],
            ['<MyUrl: test_url_2>', '<MyUrl: test_url_1>']
        )


class DetailViewTests(TestCase):

    def test_tiny_url(self):
        """
        the detail view of a exist tiny url displays the original url and the tiny url.
        """
        tiny_url = create_tiny_url('test_url')
        url = reverse('tinyurl:detail', args=(tiny_url.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, tiny_url.original_url)
        self.assertContains(response, tiny_url.tiny_url)
