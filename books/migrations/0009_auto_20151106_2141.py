# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_auto_20151106_0142'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='author_first_name',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='author_last_name',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='book_ISBN',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='current_bid',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='edition',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='id',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='price',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='start_price',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='title',
        ),
        migrations.AddField(
            model_name='listing',
            name='book_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=datetime.datetime(2015, 11, 6, 21, 41, 1, 454621, tzinfo=utc), serialize=False, to='books.Book'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='listing',
            name='start_bid',
            field=models.DecimalField(default=0, max_digits=5, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='listing',
            name='buy_it_now_price',
            field=models.DecimalField(default=0, max_digits=5, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='listing',
            name='course_num',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='listing',
            name='is_auction',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='listing',
            name='is_buy_it_now',
            field=models.BooleanField(default=True),
        ),
    ]
