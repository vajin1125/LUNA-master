# Generated by Django 2.0.4 on 2018-05-11 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Uni_Socs', '0008_events'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='description',
            field=models.TextField(max_length=100000, null=True),
        ),
        migrations.AddField(
            model_name='universities',
            name='cover_photo',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='universities',
            name='description',
            field=models.TextField(max_length=100000, null=True),
        ),
        migrations.AlterField(
            model_name='events',
            name='cover_photo',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='events',
            name='uni_socs',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Uni_Socs.Universities_Societies'),
        ),
    ]
