# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0022_auto_20151113_1758'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='book_ISBN',
        ),
        migrations.RemoveField(
            model_name='bid',
            name='listing_start_time',
        ),
        migrations.RemoveField(
            model_name='bid',
            name='seller_email',
        ),
        migrations.AddField(
            model_name='bid',
            name='listing',
            field=models.ForeignKey(default=0, to='books.Listing'),
            preserve_default=False,
        ),
    ]
