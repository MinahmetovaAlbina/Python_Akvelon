from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import MyUrl
from .hash import get_hash, get_hash_with_hashids
from .views import get_most_frequently_used


class MyUrlTests(TestCase):

    def test_MyUrl_string_is_tiny_url(self):
        """
        MyUrl string is tiny url
        :return:
        """
        my_url = MyUrl(original_url='text')
        self.assertIs(f"{my_url}", my_url.original_url)


class HashTests(TestCase):

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

    def test_hashids_from_one_id_are_same(self):
        """
        hash from one string should be equal
        """
        id = 5696332315489
        self.assertEqual(get_hash_with_hashids(id), get_hash_with_hashids(id),
                         'hash from one id are different')

    def test_hashids_from_equal_ids_are_equal(self):
        """
        hash from equal strings should be equal
        """
        id_1 = 56264894848484877777
        id_2 = id_1
        self.assertEqual(get_hash_with_hashids(id_1), get_hash_with_hashids(id_2),
                         'hash from equal ids are different')

    def test_hashids_from_different_ids_are_different(self):
        """
        hash from different strings should be different
        """
        id_1 = 85236666625878952
        id_2 = id_1 + 45415618624586322
        self.assertNotEqual(get_hash_with_hashids(id_1), get_hash_with_hashids(id_2),
                            'hash from different ids are equal')


def create_my_url(original_url, num_of_uses=0):
    """
    Create a MyUrl with the given 'tiny_url_text' and 'num_of_uses'
    :param original_url: original url
    :param num_of_uses: the number of times the tiny url was used
    :return: created MyUrl
    """
    my_url = MyUrl.objects.create(original_url=original_url, hash=0,
                                  pub_date=timezone.now(), last_us_date=timezone.now(), num_of_uses=num_of_uses)
    my_url.hash = get_hash_with_hashids(my_url.id)
    my_url.save()
    return my_url


class ViewTest(TestCase):

    def test_get_most_frequently_used(self):
        """
        get_most_frequently_used() should return MyUrls in right order
        """
        create_my_url('url_1', num_of_uses=1)
        create_my_url('url_2', num_of_uses=100)
        create_my_url('url_3', num_of_uses=10)
        self.assertQuerysetEqual(get_most_frequently_used(), ['<MyUrl: url_2>', '<MyUrl: url_3>', '<MyUrl: url_1>'])


class IndexViewTests(TestCase):

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
        """
        The index page should displayed multiple tiny urls in right order.
        """
        create_my_url(original_url='test_url_1', num_of_uses=1)
        create_my_url(original_url='test_url_2', num_of_uses=100)
        create_my_url(original_url='test_url_3', num_of_uses=10)
        response = self.client.get(reverse('tinyurl:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['most_frequently_used'],
            ['<MyUrl: test_url_2>', '<MyUrl: test_url_3>', '<MyUrl: test_url_1>']
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
        self.assertContains(response, 'Create new tiny url')


class CreatePostViewTests(TestCase):

    def test_right_create(self):
        """
        Create a tiny_url and right redirect on its detail page
        """
        text = 'test_url'
        url = reverse('tinyurl:create_post', )
        response = self.client.post(url, {'original_url': text})
        url_detail = reverse('tinyurl:detail', args=(1, ))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, url_detail)

    def test_create_already_existing_url(self):
        """
        If tiny url for this original url already exists, new tiny url don't created
        and appropriate message are displayed
        """
        my_url = create_my_url('test_url')
        url = reverse('tinyurl:create_post', )
        response = self.client.post(url, {'original_url': my_url.original_url})
        self.assertEqual(MyUrl.objects.count(), 1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create new tiny url')
        self.assertEqual(response.context['error_message'], 'I already made a tiny url for this one.')

    def test_create_with_no_url(self):
        """
        If trying create a tiny_url for no url, new tiny url don't created
        and appropriate message are displayed
        """
        url = reverse('tinyurl:create_post', )
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create new tiny url')
        self.assertEqual(response.context['error_message'], "You didn't give me any url ;(")

    def test_create_with_empty_url(self):
        """
        If trying create a tiny_url for empty url, new tiny url don't created
        and appropriate message are displayed
        """
        url = reverse('tinyurl:create_post', )
        response = self.client.post(url, {'original_url': ''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create new tiny url')
        self.assertEqual(response.context['error_message'], "You didn't give me any url ;(")


class DeleteViewTests(TestCase):

    def test_delete_only_url(self):
        """
        Delete only MyUrl
        """
        create_my_url('test_url')
        url = reverse('tinyurl:delete', )
        response = self.client.post(url, {'deleted_url_id': 1})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tiny URL has been deleted successfully.')
        self.assertContains(response, 'No tiny url has been added.')

    def test_delete_one_of_two_urls(self):
        """
        Delete one MyUrl
        """
        create_my_url('test_url_1')
        create_my_url('test_url_2')
        url = reverse('tinyurl:delete', )
        response = self.client.post(url, {'deleted_url_id': 1})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tiny URL has been deleted successfully.')
        self.assertQuerysetEqual(
            response.context['most_frequently_used'],
            ['<MyUrl: test_url_2>']
        )

    def test_delete_without_choice(self):
        """
        If no MyUrl has been selected for deleting, view should displayed appropriated error message
        """
        my_url = create_my_url('test_url')
        url = reverse('tinyurl:delete', )
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['most_frequently_used'], ['<MyUrl: test_url>'])
        self.assertEqual(response.context['error_message'], "You haven't selected anything to delete.")


class TinyUrlViewTest(TestCase):

    def test_tiny_url_redirect_right(self):
        """
        tiny url redirects on original url and increase number of its uses
        """
        original_url = 'https://duckduckgo.com'
        my_url = create_my_url(original_url)
        url = reverse('tinyurl:tiny_url', args=(my_url.hash, ))
        response = self.client.get(url)
        updated_mu_url = MyUrl.objects.get(pk=my_url.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, original_url, "the tiny url doesn't redirect to the original url")
        self.assertEqual(updated_mu_url.num_of_uses, 1)

    def test_tiny_url_with_wrong_url(self):
        """
        Trying redirect on wrong hash returns a 404 not found.
        """
        url = reverse('tinyurl:tiny_url', args=(1, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
