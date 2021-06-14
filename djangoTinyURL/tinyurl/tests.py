from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import MyUrl
from .hash import get_hash
from .views import IndexView


class MyUrlTests(TestCase):

    def test_MyUrl_string_is_tiny_url(self):
        """
        MyUrl string is tiny url
        :return:
        """
        my_url = MyUrl(original_url='text')
        self.assertIs(f"{my_url}", my_url.original_url)


class HashTests(TestCase):

    def test_get_hash(self):
        text = 'test'
        self.assertEqual(get_hash(text), f"{text.__hash__()}")

    def test_hash_from_one_strings_are_same(self):
        """
        hash from one string should be equal
        """
        text = 'test'
        self.assertEqual(get_hash(text), get_hash(text), 'hash from one string are different')

    def test_hash_from_equal_strings_are_equal(self):
        """
        hash from equal strings should be equal
        """
        text1 = 'test'
        text2 = text1
        self.assertEqual(get_hash(text1), get_hash(text2), 'hash from equal string are different')

    def test_hash_from_different_strings_are_different(self):
        """
        hash from different strings should be different
        """
        text1 = 'test'
        text2 = text1 + '4'
        self.assertNotEqual(get_hash(text1), get_hash(text2), 'hash from different string are equal')


def create_my_url(original_url, num_of_uses=0):
    """
    Create a MyUrl with the given 'tiny_url_text' and 'num_of_uses'
    :param original_url: original url
    :param num_of_uses: the number of times the tiny url was used
    :return: created MyUrl
    """
    return MyUrl.objects.create(original_url=original_url, hash=get_hash(original_url),
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
        create_my_url(original_url='test_url')
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
        create_my_url(original_url='test_url_1', num_of_uses=1)
        create_my_url(original_url='test_url_2', num_of_uses=10)
        response = self.client.get(reverse('tinyurl:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['most_frequently_used'],
            ['<MyUrl: test_url_2>', '<MyUrl: test_url_1>']
        )

    def test_right_order_in_queryset(self):
        create_my_url(original_url='test_url_1', num_of_uses=1)
        create_my_url(original_url='test_url_2', num_of_uses=10)
        create_my_url(original_url='test_url_3', num_of_uses=100)
        response = self.client.get(reverse('tinyurl:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['most_frequently_used'],
            ['<MyUrl: test_url_3>', '<MyUrl: test_url_2>', '<MyUrl: test_url_1>']
        )


class DetailViewTests(TestCase):

    def test_tiny_url(self):
        """
        the detail view of a exist tiny url displays the original url and the tiny url.
        """
        tiny_url = create_my_url('test_url')
        url = reverse('tinyurl:detail', args=(tiny_url.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, tiny_url.original_url)
        self.assertContains(response, tiny_url.get_tiny_url())


class CreateViewTests(TestCase):

    def test_create_page_are_allowed(self):
        url = reverse('tinyurl:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TinyUrlViewTest(TestCase):

    def test_tiny_url_redirect_right(self):
        """
        tiny url redirects on original url
        """
        original_url = 'https://duckduckgo.com'
        my_url = create_my_url(original_url)
        url = reverse('tinyurl:tiny_url', args=(my_url.hash, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.url, original_url, "the tiny url doesn't redirect to the original url")
