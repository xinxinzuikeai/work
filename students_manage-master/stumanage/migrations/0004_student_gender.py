# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stumanage', '0003_auto_20170823_1122'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='gender',
            field=models.BooleanField(default=True, verbose_name='\u6027\u522b'),
        ),
    ]
