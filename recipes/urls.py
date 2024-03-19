from django.urls import path
from .views import *

urlpatterns = [
    path('categories/', RecipeCategoriesListAPIView.as_view(), name='recipe_categories'),
    path('categories/<int:pk>/', CategoryRecipesListAPIView.as_view(), name='category_recipes'),
    path('', RecipesListAPIView.as_view(), name='recipes'),
    path('<int:pk>/', RecipeInfoAPIView.as_view(), name='recipe_info'),
    path('create/', RecipePostAPIView.as_view(), name='recipe_create'),
    path('<int:pk>/like/', RecipeLikeAPIView.as_view(), name='recipe_like'),
    path('<int:pk>/unlike/', RecipeUnlikeAPIView.as_view(), name='recipe_unlike'),
    path('<int:pk>/save/', RecipeSaveAPIView.as_view(), name='recipe_save'),
    path('<int:pk>/unsave/', RecipeUnsaveAPIView.as_view(), name='recipe_unsave'),
]
