# Generated by Django 5.0.6 on 2024-06-08 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_alter_customerbook_returned'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='ISBN',
            field=models.CharField(help_text="Book's ISBN", max_length=250, unique=True),
        ),
    ]