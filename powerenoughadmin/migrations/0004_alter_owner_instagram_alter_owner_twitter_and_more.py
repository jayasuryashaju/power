# Generated by Django 5.0.1 on 2024-02-18 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('powerenoughadmin', '0003_alter_owner_address_alter_owner_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='owner',
            name='instagram',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='owner',
            name='twitter',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='owner',
            name='whatsapp',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='owner',
            name='youtube',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
