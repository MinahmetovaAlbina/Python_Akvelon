# Generated by Django 3.2.4 on 2021-06-13 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tinyurl', '0004_auto_20210613_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myurl',
            name='last_us_date',
            field=models.DateTimeField(verbose_name='date of last using of url'),
        ),
    ]
