from django.db import models
from django.urls import reverse


def get_tiny_url_page_url():
    c = '*'
    return 'http://127.0.0.1:8000' + reverse('tinyurl:tiny_url', args=(c, )).strip(c)


class MyUrl(models.Model):
    original_url = models.CharField(max_length=200)
    hash = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    last_us_date = models.DateTimeField('date of last using of url')
    num_of_uses = models.IntegerField('the number of times the tiny url was used', default=0)

    def __str__(self):
        return self.original_url

    def get_tiny_url(self):
        return get_tiny_url_page_url() + self.hash



