# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-01 06:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_article_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='index',
            field=models.IntegerField(default=1, verbose_name='分类的排序'),
        ),
    ]
