from django.urls import reverse
import hashlib
from hashids import Hashids


Salt = '^-^_<3'


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
    hashids = Hashids(salt=Salt, min_length=4)
    return hashids.encode(id)
