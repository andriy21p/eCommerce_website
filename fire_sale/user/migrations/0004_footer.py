# Generated by Django 4.0.4 on 2022-05-13 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_rename_name_profile_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Footer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=10000)),
                ('footer_page', models.CharField(choices=[(1, 'Conduct'), (2, 'Privacy'), (3, 'Security'), (4, 'Cookies')], max_length=100)),
                ('created', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
