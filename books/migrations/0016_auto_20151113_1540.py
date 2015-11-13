# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0015_auto_20151112_2051'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author_first_name', models.CharField(max_length=200, null=True)),
                ('author_last_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='book',
            name='author_first_name',
        ),
        migrations.RemoveField(
            model_name='book',
            name='author_last_name',
        ),
        migrations.AddField(
            model_name='author',
            name='book_ISBN',
            field=models.ForeignKey(to='books.Book'),
        ),
    ]
