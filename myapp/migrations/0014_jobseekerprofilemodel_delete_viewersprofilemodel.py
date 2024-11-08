# Generated by Django 5.1.2 on 2024-10-27 05:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_remove_applyjobmodel_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='jobseekerProfileModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Skills', models.CharField(choices=[('programing', 'Programing'), ('graphics_design', 'Graphics Design'), ('resarch', 'Resarch')], max_length=255, null=True)),
                ('Image', models.ImageField(null=True, upload_to='Media/Blog_Pic')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='viewersProfile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='viewersProfileModel',
        ),
    ]
