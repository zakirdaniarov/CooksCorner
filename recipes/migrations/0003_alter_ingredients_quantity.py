# Generated by Django 5.0.3 on 2024-03-19 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredients',
            name='quantity',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
