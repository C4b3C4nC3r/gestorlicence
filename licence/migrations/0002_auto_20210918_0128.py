# Generated by Django 3.2.7 on 2021-09-18 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licence', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='codelicence',
            name='date_rem',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='codelicence',
            name='create_at',
            field=models.DateTimeField(null=True),
        ),
    ]
