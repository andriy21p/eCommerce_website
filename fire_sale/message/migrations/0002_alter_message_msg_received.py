# Generated by Django 4.0.4 on 2022-05-05 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='msg_received',
            field=models.DateTimeField(null=True),
        ),
    ]