# Generated by Django 5.1.2 on 2024-10-14 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=50)),
                ('middleName', models.CharField(blank=True, max_length=50)),
                ('lastName', models.CharField(max_length=50)),
                ('resumptionDate', models.DateField(default=None, null=True)),
                ('vacationDate', models.DateField(default=None, null=True)),
            ],
            options={
                'ordering': ['firstName', 'middleName', 'lastName'],
            },
        ),
    ]
