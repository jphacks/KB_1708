# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-21 15:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import ghostwriter.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='タイトル')),
                ('image', models.ImageField(upload_to=ghostwriter.models.get_image_path, verbose_name='Image')),
                ('ocr', models.TextField(blank=True, null=True, verbose_name='OCR')),
            ],
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='タイトル')),
                ('day_of_week', models.IntegerField(choices=[(0, '集中'), (1, '月曜日'), (2, '火曜日'), (3, '水曜日'), (4, '木曜日'), (5, '金曜日'), (6, '土曜日'), (7, '日曜日')], verbose_name='曜日')),
                ('period', models.IntegerField(choices=[(1, '1限'), (2, '2限'), (3, '3限'), (4, '4限'), (5, '5限'), (6, '6限')], verbose_name='時限')),
            ],
        ),
        migrations.AddField(
            model_name='image',
            name='lecture',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='ghostwriter.Lecture'),
        ),
    ]