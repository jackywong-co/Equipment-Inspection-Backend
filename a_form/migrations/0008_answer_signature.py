# Generated by Django 4.0.2 on 2022-04-06 17:29

import a_form.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_form', '0007_equipmentimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='signature',
            field=models.ImageField(blank=True, null=True, upload_to=a_form.models.path_and_rename_to_record_signature),
        ),
    ]