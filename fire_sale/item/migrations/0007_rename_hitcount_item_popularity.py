# Generated by Django 4.0.4 on 2022-05-04 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0006_item_hitcount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='hitcount',
            new_name='popularity',
        ),
    ]
