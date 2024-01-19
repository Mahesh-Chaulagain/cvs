# Generated by Django 3.1.3 on 2021-09-25 02:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0009_auto_20210703_1159'),
    ]

    operations = [
        migrations.CreateModel(
            name='SetVoteDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voting_start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('voting_duration', models.DurationField()),
                ('voting_end_date', models.DateTimeField()),
                ('registration_start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('registration_duration', models.DurationField()),
                ('registration_end_date', models.DateTimeField()),
            ],
        ),
        migrations.DeleteModel(
            name='SetDate',
        ),
    ]