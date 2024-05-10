# Generated by Django 5.0.1 on 2024-05-10 12:22

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('visit_count', models.IntegerField(default=0)),
                ('unique_visitors', models.IntegerField(default=0)),
            ],
        ),
    ]