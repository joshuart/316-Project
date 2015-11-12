# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0014_auto_20151112_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='is_buy_it_now',
            field=models.BooleanField(default=True),
        ),
    ]
