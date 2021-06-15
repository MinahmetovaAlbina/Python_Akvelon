from django.urls import reverse
import hashlib
from hashids import Hashids


def get_hash(original_url: str):
    """
    Generate hash for the given 'original_url'
    :param original_url: url
    :return: hash: string
    """
    return f'{original_url.__hash__()}'


def get_hash_with_hashids(id: int):
    """
    Generate hash for the given 'original_url' with using hashides
    :param id: id of MyUrl
    :return: hash: string
    """
    hashids = Hashids(salt='^-^_<3', min_length=4)
    return hashids.encode(id)
