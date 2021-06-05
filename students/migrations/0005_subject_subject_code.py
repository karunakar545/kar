# Generated by Django 3.2.3 on 2021-06-05 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_auto_20210605_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='subject_code',
            field=models.CharField(default='jkgf', help_text='Enter Subject Code <b>Given by SPPU</b>', max_length=10, unique=True),
            preserve_default=False,
        ),
    ]
