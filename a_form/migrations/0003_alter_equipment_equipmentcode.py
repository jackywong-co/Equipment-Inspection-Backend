# Generated by Django 4.0.1 on 2022-01-16 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_form', '0002_alter_equipment_equipmentcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='equipmentCode',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]