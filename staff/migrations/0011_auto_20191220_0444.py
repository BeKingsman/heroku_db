# Generated by Django 2.2.6 on 2019-12-20 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0010_auto_20191219_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_profile',
            name='Password',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='user_profile',
            name='username',
            field=models.CharField(max_length=200, null=True),
        ),
    ]