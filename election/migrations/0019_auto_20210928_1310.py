# Generated by Django 3.1.3 on 2021-09-28 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0018_auto_20210928_1052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='approved_result',
        ),
        migrations.AddField(
            model_name='result',
            name='published_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]