# Generated by Django 2.0.4 on 2018-05-09 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_auto_20180509_1427'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lunausers',
            old_name='uni_id',
            new_name='uni',
        ),
    ]