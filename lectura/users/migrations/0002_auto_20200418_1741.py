# Generated by Django 3.0.2 on 2020-04-18 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar_url',
            field=models.URLField(blank=True, default='https://i.imgur.com/m0cVFB2.jpg', verbose_name='label_avatar_url'),
        ),
    ]
