# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0017_auto_20151113_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='course_num',
            field=models.PositiveSmallIntegerField(default=101),
        ),
    ]
