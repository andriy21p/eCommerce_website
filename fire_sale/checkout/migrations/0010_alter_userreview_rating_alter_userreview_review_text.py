# Generated by Django 4.0.4 on 2022-05-13 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0009_userreview_seller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userreview',
            name='rating',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, '★☆☆☆☆'), (2, '★★☆☆☆'), (3, '★★★☆☆'), (4, '★★★★☆'), (5, '★★★★★')]),
        ),
        migrations.AlterField(
            model_name='userreview',
            name='review_text',
            field=models.TextField(blank=True, help_text='Please write your review here...', max_length=10000),
        ),
    ]
