# Generated by Django 5.1.3 on 2024-12-13 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0020_delete_result'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElectionDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result_date', models.DateTimeField(verbose_name='Result Date')),
            ],
        ),
    ]