# Generated by Django 3.1.3 on 2021-06-03 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0005_auto_20210502_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='candidate_images/', verbose_name='Candidate Pic'),
        ),
    ]
