# Generated by Django 2.0.4 on 2018-05-09 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Uni_Socs', '0002_universities_domain'),
    ]

    operations = [
        migrations.CreateModel(
            name='Universities_Societies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_uni', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Uni_Socs.Universities')),
            ],
        ),
    ]