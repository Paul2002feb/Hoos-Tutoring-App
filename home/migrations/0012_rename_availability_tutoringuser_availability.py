# Generated by Django 4.1.6 on 2023-04-03 22:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_rename_availability_tutoringuser_availability'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tutoringuser',
            old_name='availability',
            new_name='Availability',
        ),
    ]
