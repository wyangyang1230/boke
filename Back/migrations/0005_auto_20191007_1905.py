# Generated by Django 2.2.1 on 2019-10-07 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Back', '0004_auto_20191007_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date',
            field=models.DateTimeField(auto_now=True, verbose_name='文章日期'),
        ),
    ]
