# Generated by Django 5.0 on 2023-12-05 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managesystemvendor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='contact_details',
            field=models.CharField(max_length=10),
        ),
    ]
