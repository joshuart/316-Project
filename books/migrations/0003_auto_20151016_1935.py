# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20151013_1811'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='first_name',
            field=models.CharField(default='first', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='seller',
            name='last_name',
            field=models.CharField(default='last', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='book',
            name='author_first_name',
            field=models.CharField(default='a_first', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterModelTable(
            name='book',
            table='book',
        ),
        migrations.AlterModelTable(
            name='seller',
            table='seller',
        ),
    ]
