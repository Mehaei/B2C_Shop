# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-21 14:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0002_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Types',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('pid', models.IntegerField()),
                ('path', models.CharField(max_length=50)),
            ],
        ),
    ]
