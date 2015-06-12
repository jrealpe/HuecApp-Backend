# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='image_restaurant',
            field=models.ImageField(null=True, upload_to=b'restaurants/'),
        ),
        migrations.AddField(
            model_name='restaurantdish',
            name='image_dish',
            field=models.ImageField(null=True, upload_to=b'restaurants/'),
        ),
    ]
