# Generated by Django 4.2.1 on 2024-12-07 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_student_section'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='section',
            field=models.CharField(choices=[('complexe', 'Complexe Coranique'), ('institut', 'Institut Coranique')], db_index=True, default='complexe', max_length=20, verbose_name='Section'),
        ),
    ]
