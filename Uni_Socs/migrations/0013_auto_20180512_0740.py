# Generated by Django 2.0.4 on 2018-05-12 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Uni_Socs', '0012_auto_20180511_1341'),
    ]

    operations = [
        migrations.AddField(
            model_name='universities_societies',
            name='cover_photo',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='universities_societies',
            name='description',
            field=models.TextField(max_length=100000, null=True),
        ),
    ]