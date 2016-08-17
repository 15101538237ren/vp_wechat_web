# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voiceprint', '0002_user_step'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='step',
            field=models.IntegerField(default=1, null=True),
        ),
    ]
