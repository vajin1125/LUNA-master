# Generated by Django 2.0.4 on 2018-05-11 08:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Uni_Socs', '0009_auto_20180511_0756'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='events',
            name='details',
        ),
    ]
