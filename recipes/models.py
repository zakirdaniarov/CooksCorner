from django.db import models
from users.models import User

# Create your models here.
DIFFICULTY = (('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard'),)


class RecipeCategories(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    name = models.CharField(max_length=150)
    # quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    quantity = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name}-{self.quantity}'


class Recipe(models.Model):
    recipe_name = models.CharField(max_length=200)
    category = models.ManyToManyField(RecipeCategories, related_name='recipes')
    cooking_time = models.CharField(max_length=50)
    difficulty = models.CharField(max_length=100, choices=DIFFICULTY, default='Easy')
    cooker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipe')
    description = models.TextField()
    ingredients = models.ManyToManyField(Ingredients, related_name='for_recipe')
    image = models.ImageField(upload_to='recipe_photos', blank=True, null=True)
    liked_user = models.ManyToManyField(User, through='Like', blank=True, related_name='liked_recipes')
    saved_user = models.ManyToManyField(User, through='Save', blank=True, related_name='saved_recipes')

    def __str__(self):
        return f'{self.recipe_name} from {self.cooker}'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe')


class Save(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe')





