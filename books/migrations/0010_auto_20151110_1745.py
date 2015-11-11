# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0009_auto_20151106_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='book_ISBN',
            field=models.ForeignKey(to='books.Listing'),
        ),
    ]
