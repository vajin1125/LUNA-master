# Generated by Django 2.0.4 on 2018-05-17 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0005_auto_20180512_0740'),
    ]

    operations = [
        migrations.AddField(
            model_name='lunausers',
            name='security_key',
            field=models.CharField(default='asdfjkl;', max_length=100),
            preserve_default=False,
        ),
    ]
