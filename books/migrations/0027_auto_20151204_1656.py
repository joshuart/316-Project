# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0026_auto_20151204_1454'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='course_dept',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='course_num',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='professor',
        ),
    ]
