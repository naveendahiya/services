# Generated by Django 3.0.5 on 2020-09-03 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='pincode',
            field=models.IntegerField(null=True),
        ),
    ]
