from django.urls import reverse


def get_index_page_url():
    return 'http://127.0.0.1:8000' + reverse('tinyurl:index')


def get_tiny_url(my_hash: str):
    return get_index_page_url() + ':3/' + my_hash


def get_hash(original_url: str):
    return f'{original_url.__hash__()}'
