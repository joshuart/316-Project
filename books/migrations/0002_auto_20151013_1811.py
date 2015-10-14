# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='isbn10',
            new_name='isbn',
        ),
        migrations.RemoveField(
            model_name='book',
            name='isbn13',
        ),
        migrations.RemoveField(
            model_name='seller',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='seller',
            name='last_name',
        ),
        migrations.AddField(
            model_name='book',
            name='author_first_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='author_last_name',
            field=models.CharField(default='test', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='title',
            field=models.CharField(default='test', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='seller',
            name='email',
            field=models.EmailField(max_length=200),
        ),
    ]
