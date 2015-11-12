# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0012_listing_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='bid_time',
            field=models.IntegerField(verbose_name=b'bid time'),
        ),
        migrations.AlterField(
            model_name='bid',
            name='listing_start_time',
            field=models.IntegerField(verbose_name=b'date posted'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='start_time',
            field=models.IntegerField(verbose_name=b'date posted'),
        ),
    ]
