# Generated by Django 4.1.5 on 2023-01-27 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
                ('age', models.IntegerField(default=18)),
                ('father_name', models.CharField(default='', max_length=255)),
            ],
        ),
    ]
