# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, verbose_name='\u73ed\u7ea7\u540d\u5b57')),
                ('pub_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': '\u73ed\u7ea7',
                'verbose_name_plural': '\u73ed\u7ea7',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, verbose_name='\u5b66\u751f\u59d3\u540d')),
                ('age', models.IntegerField(verbose_name='\u5b66\u751f\u5e74\u9f84')),
                ('score', models.DecimalField(null=True, verbose_name='\u5b66\u751f\u6210\u7ee9', max_digits=5, decimal_places=2, blank=True)),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='\u5b66\u751f\u90ae\u7bb1', blank=True)),
                ('tel', models.BigIntegerField(verbose_name='\u5b66\u751f\u7535\u8bdd')),
                ('pub_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('className', models.ForeignKey(to='stumanage.Class')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': '\u5b66\u751f',
                'verbose_name_plural': '\u5b66\u751f',
            },
        ),
    ]
