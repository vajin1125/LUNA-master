# Generated by Django 2.0.4 on 2018-05-14 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Uni_Socs', '0013_auto_20180512_0740'),
    ]

    operations = [
        migrations.AddField(
            model_name='universities_societies',
            name='about',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='universities_societies',
            name='phone',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='universities_societies',
            name='web_site',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
