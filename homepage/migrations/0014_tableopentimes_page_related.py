# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-07 20:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0013_auto_20170607_2350'),
    ]

    operations = [
        migrations.AddField(
            model_name='tableopentimes',
            name='page_related',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='homepage.IndexPage'),
        ),
    ]