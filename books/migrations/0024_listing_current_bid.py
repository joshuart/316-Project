# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0023_auto_20151204_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='current_bid',
            field=models.IntegerField(default=0),
        ),
    ]
