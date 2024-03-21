from django.db import migrations
from decimal import Decimal


def convert_quantity_to_charfield(apps, schema_editor):
    Ingredients = apps.get_model('recipes', 'Ingredients')

    # Iterate through each Ingredients object
    for ingredient in Ingredients.objects.all():
        # Convert the decimal quantity to a string
        ingredient.quantity = str(ingredient.quantity)
        ingredient.save()


class Migration(migrations.Migration):
    dependencies = [
        ('recipes', '0003_alter_ingredients_quantity'),  # Change this to the previous migration file
    ]

    operations = [
        migrations.RunPython(convert_quantity_to_charfield),
    ]
