from django.contrib import admin
from .models import *

admin.site.register(RecipeCategories)
admin.site.register(Recipe)
admin.site.register(Ingredients)

