# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voiceprint', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='step',
            field=models.IntegerField(default=1),
        ),
    ]
