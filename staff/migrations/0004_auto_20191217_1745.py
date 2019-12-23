# Generated by Django 2.2.6 on 2019-12-17 17:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('staff', '0003_remove_staff_excel_uploaded_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_excel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sheet', models.FileField(upload_to='')),
                ('uploaded_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='excel_sheets', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RenameModel(
            old_name='Staff_profile',
            new_name='user_profile',
        ),
        migrations.DeleteModel(
            name='staff_excel',
        ),
    ]
