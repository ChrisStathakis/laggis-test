# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-30 13:43
from __future__ import unicode_literals

import blog.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('image', models.FileField(blank=True, upload_to=blog.models.upload_file, verbose_name='Image - not used atm')),
                ('content', models.TextField(verbose_name='Short description or Intro')),
                ('publish', models.DateField(auto_now=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(allow_unicode=True, blank=True, null=True, unique=True, verbose_name='Slug - Dont bother with that ')),
                ('seo', models.CharField(blank=True, max_length=100)),
                ('meta_description', models.CharField(blank=True, max_length=100)),
                ('announcement', models.BooleanField(default=False)),
                ('title_eng', models.CharField(default='English', max_length=100, verbose_name='Title')),
                ('content_eng', models.TextField(default='English', verbose_name='Short description or Intro')),
            ],
            managers=[
                ('my_query', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(allow_unicode=True, blank=True, null=True)),
                ('content', models.CharField(blank=True, max_length=150, null=True)),
                ('title_eng', models.CharField(default='English', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PostTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('title_eng', models.CharField(default='English', max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.PostCategory'),
        ),
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='post_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='blog.PostTags'),
        ),
    ]