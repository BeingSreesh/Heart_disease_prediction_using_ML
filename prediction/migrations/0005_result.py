# Generated by Django 2.2.1 on 2020-01-27 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prediction', '0004_auto_20200127_0738'),
    ]

    operations = [
        migrations.CreateModel(
            name='result',
            fields=[
                ('patientid', models.IntegerField(default=False, primary_key=True, serialize=False)),
                ('results', models.CharField(default=False, max_length=100)),
            ],
        ),
    ]