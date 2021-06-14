from django.db import models
from django.urls import reverse


class MyUrl(models.Model):
    original_url = models.CharField(max_length=200)
    tiny_url = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    last_us_date = models.DateTimeField('date of last using of url')
    num_of_uses = models.IntegerField('the number of times the tiny url was used', default=0)

    def __str__(self):
        return self.tiny_url

    def get_absolute_url(self):
        return reverse('tinyurl:detail', kwargs={'pk': self.pk})
