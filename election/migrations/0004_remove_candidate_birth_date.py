# Generated by Django 3.1.3 on 2021-05-02 02:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0003_auto_20210502_0822'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidate',
            name='birth_date',
        ),
    ]