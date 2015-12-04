# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0024_listing_current_bid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='book_ptr',
        ),
        migrations.AddField(
            model_name='listing',
            name='book',
            field=models.ForeignKey(default=0, to='books.Book'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='listing',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=0, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
