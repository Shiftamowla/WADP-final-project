# Generated by Django 5.1.2 on 2024-11-08 13:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0019_alter_applyjobmodel_skills_alter_jobmodel_skills'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.jobmodel')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
