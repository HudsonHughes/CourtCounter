# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-17 19:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('court_counter', '0002_auto_20171017_0010'),
    ]

    operations = [
        migrations.CreateModel(
            name='file',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=144)),
                ('last_modified', models.DateTimeField(auto_now_add=True)),
                ('count', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='shot',
            name='metric',
            field=models.BooleanField(default=False),
        ),
    ]