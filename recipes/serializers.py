from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *


class CategoryListAPI(ModelSerializer):
    class Meta:
        model = RecipeCategories
        fields = ['id', 'name']


class RecipeListAPI(ModelSerializer):
    total_likes = serializers.SerializerMethodField(default=0)
    total_saves = serializers.SerializerMethodField(default=0)

    class Meta:
        model = Recipe
        fields = ['id', 'recipe_name', 'category', 'cooker', 'image', 'total_likes', 'total_saves']

    def get_total_likes(self, instance):
        return instance.liked_user.all().count()

    def get_total_saves(self, instance):
        return instance.saved_user.all().count()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ['name', 'quantity']


class RecipeDetailAPI(ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    is_liked = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField(default=0)
    total_saves = serializers.SerializerMethodField(default=0)

    class Meta:
        model = Recipe
        fields = ['id', 'recipe_name', 'category', 'cooking_time', 'difficulty', 'cooker', 'description', 'ingredients', 'image', 'is_liked', 'is_saved', 'total_likes', 'total_saves']

    def get_total_likes(self, instance):
        return instance.liked_user.all().count()

    def get_total_saves(self, instance):
        return instance.saved_user.all().count()

    def get_is_liked(self, instance):
        user = self.context['request'].user
        return instance.liked_user.filter(id=user.id).exists()

    def get_is_saved(self, instance):
        user = self.context['request'].user
        return instance.saved_user.filter(id=user.id).exists()


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ['id', 'name', 'quantity']


class RecipePostAPI(serializers.ModelSerializer):
    ingredients = IngredientsSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ['id', 'recipe_name', 'cooking_time', 'difficulty', 'description', 'ingredients', 'image', 'category']

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        category_data = validated_data.pop('category')
        cooker = self.context['request'].user  # Get the user making the request

        recipe = Recipe.objects.create(cooker=cooker, **validated_data)
        recipe.category.set(category_data)

        return recipe




