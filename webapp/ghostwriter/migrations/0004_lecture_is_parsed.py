# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-09 05:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ghostwriter', '0003_auto_20171022_0821'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='is_parsed',
            field=models.BooleanField(default=True, verbose_name='Is Parsed'),
        ),
    ]