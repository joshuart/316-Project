# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_auto_20151019_1745'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='password',
            new_name='password1',
        ),
        migrations.AddField(
            model_name='user',
            name='password2',
            field=models.CharField(default=123, max_length=200),
            preserve_default=False,
        ),
    ]
