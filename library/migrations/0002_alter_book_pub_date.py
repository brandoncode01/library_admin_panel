# Generated by Django 5.0.6 on 2024-05-22 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='pub_date',
            field=models.DateField(help_text='Date when book was published'),
        ),
    ]
