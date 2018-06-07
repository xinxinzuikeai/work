# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stumanage', '0002_userprofile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'ordering': ['id'], 'verbose_name': '\u7cfb\u7edf\u7528\u6237\u62d3\u5c55\u8868', 'verbose_name_plural': '\u7cfb\u7edf\u7528\u6237\u62d3\u5c55\u8868'},
        ),
        migrations.AddField(
            model_name='student',
            name='avatar',
            field=models.ImageField(default='avatar/default.jpg', upload_to='avatar/', verbose_name='\u5934\u50cf'),
        ),
    ]
