from django.urls import reverse


def get_hash(original_url: str):
    """
    Generate hash for the given 'original_url'
    :param original_url: url
    :return: hash: string
    """
    return f'{original_url.__hash__()}'
