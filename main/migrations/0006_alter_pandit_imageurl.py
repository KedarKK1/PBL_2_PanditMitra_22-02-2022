# Generated by Django 3.2.6 on 2022-04-24 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_pandit_imageurl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pandit',
            name='imageUrl',
            field=models.TextField(max_length=2000, verbose_name='Pandit Img Url'),
        ),
    ]
