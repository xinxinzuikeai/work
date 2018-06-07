# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stumanage', '0004_student_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='isDelete',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u5df2\u5220\u9664'),
        ),
        migrations.AddField(
            model_name='student',
            name='isDelete',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u5df2\u5220\u9664'),
        ),
        migrations.AlterModelTable(
            name='student',
            table='student',
        ),
    ]
