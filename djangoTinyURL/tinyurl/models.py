from django.db import models


class MyUrl(models.Model):
    original_url = models.CharField(max_length=200)
    tiny_url = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    last_us_date = models.DateTimeField('date of last using of url')
    num_of_uses = models.IntegerField('number of times tiny url was used', default=0)

    def __str__(self):
        return self.tiny_url
