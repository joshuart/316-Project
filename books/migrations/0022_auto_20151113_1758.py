# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0021_auto_20151113_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='edition',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='listing',
            name='buy_it_now_price',
            field=models.DecimalField(default=0, max_digits=5, decimal_places=2, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
