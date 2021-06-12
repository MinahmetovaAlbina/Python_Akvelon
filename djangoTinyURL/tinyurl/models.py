from django.db import models
from django.utils import timezone


class MyUrl(models.Model):
    original_url = models.CharField(max_length=200)
    tiny_url = models.CharField(max_length=200, default=original_url)
    pub_date = models.DateTimeField('date published', default=timezone.now())
    last_us_date = models.DateTimeField('date of last using of url', default=pub_date)
    num_of_uses = models.IntegerField('number of times tiny url was used', default=0)
