# Generated by Django 3.1.3 on 2021-09-28 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0014_auto_20210925_1146'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublishResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approve_result', models.BooleanField(default=False)),
            ],
        ),
    ]