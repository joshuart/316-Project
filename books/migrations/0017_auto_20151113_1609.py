# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0016_auto_20151113_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='edition',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.TextField(max_length=500, null=True),
        ),
    ]
