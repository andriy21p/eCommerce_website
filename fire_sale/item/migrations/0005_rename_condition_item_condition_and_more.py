# Generated by Django 4.0.4 on 2022-05-03 22:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0004_itemcategory_icon_itemcategory_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='Condition',
            new_name='condition',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='Description',
            new_name='description',
        ),
    ]