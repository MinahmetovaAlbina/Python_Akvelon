# Generated by Django 3.2.4 on 2021-06-12 20:47

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUrl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_url', models.CharField(max_length=200)),
                ('tiny_url', models.CharField(default=models.CharField(max_length=200), max_length=200)),
                ('pub_date', models.DateTimeField(default=datetime.datetime(2021, 6, 12, 20, 47, 0, 429017, tzinfo=utc), verbose_name='date published')),
                ('last_us_date', models.DateTimeField(default=models.DateTimeField(default=datetime.datetime(2021, 6, 12, 20, 47, 0, 429017, tzinfo=utc), verbose_name='date published'), verbose_name='date of last using of url')),
                ('num_of_uses', models.IntegerField(default=0, verbose_name='number of times tiny url was used')),
            ],
        ),
    ]