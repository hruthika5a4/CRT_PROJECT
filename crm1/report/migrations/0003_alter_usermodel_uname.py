# Generated by Django 5.0.1 on 2024-02-07 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0002_usermodel_uname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='uname',
            field=models.CharField(default='xyz', max_length=100),
        ),
    ]
