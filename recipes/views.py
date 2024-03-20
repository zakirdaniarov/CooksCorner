from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.views import Response, status, APIView
from .models import Recipe, RecipeCategories, Like,  Save
from .serializers import *
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class RecipeCategoriesListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
            summary="Displaying lists of recipe categories",
            description="This endpoint allows you to get information about various recipe categories",
    )
    def get(self, request, *args, **kwargs):
        categories = RecipeCategories.objects.all()
        categories_api = CategoryListAPI(categories, many=True)
        content = {"Categories": categories_api.data}
        return Response(content, status=status.HTTP_200_OK)


class CategoryRecipesListAPIView(APIView):
    serializer_class = RecipeCategories
    permission_classes = [IsAuthenticated]

    @extend_schema(
            summary="Displaying lists of recipes in each category",
            description="This endpoint allows you to get information about recipes in each category",
    )
    def get(self, request, *args, **kwargs):
        category = self.serializer_class.objects.all().get(id=kwargs['pk'])
        recipes = category.recipes.all()
        recipes_api = RecipeListAPI(recipes, many=True)
        content = {"Category Recipes": recipes_api.data}
        return Response(content, status=status.HTTP_200_OK)


class RecipesListAPIView(APIView):
    serializer_class = RecipeListAPI
    permission_classes = [IsAuthenticated]
    @extend_schema(
            summary="Displaying lists of recipes",
            description="This endpoint allows you to get information about total list of recipes",
    )

    def get(self, request, *args, **kwargs):
        # Get the search query parameter from the request
        search_query = request.query_params.get('search', None)

        if search_query:
            # Filter recipes based on search query
            recipes = Recipe.objects.filter(
                Q(recipe_name__icontains=search_query)
            )
        else:
            # If no search query provided, return all recipes
            recipes = Recipe.objects.all()

        recipes_api = self.serializer_class(recipes, many=True)
        content = {"Recipes": recipes_api.data}
        return Response(content, status=status.HTTP_200_OK)


class RecipeInfoAPIView(APIView):
    serializer_class = RecipeDetailAPI
    permission_classes = [IsAuthenticated]

    @extend_schema(
            summary="Displaying detailed information about the recipe",
            description="This endpoint allows you to get detailed information about the recipe: name, image,"
                        "cooker, difficulty, description and ingredients",
    )
    def get(self, request, *args, **kwargs):
        try:
            recipe = Recipe.objects.all().get(id=kwargs['pk'])
        except:
            return Response({'data': 'Page not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(recipe, context={'request': request})

        if request.user in recipe.liked_user.all():
            serializer.data['is_liked'] = True

        if request.user in recipe.saved_user.all():
            serializer.data['is_saved'] = True
        content = {"Recipe Info": serializer.data}
        return Response(content, status=status.HTTP_200_OK)


class RecipePostAPIView(APIView):
    serializer_class = RecipePostAPI
    permission_classes = [IsAuthenticated]
    @extend_schema(
            summary="Publishing new recipe",
            description="This endpoint allows you to publish new recipe",
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            recipe = serializer.save()

            # Process ingredients data
            ingredients_data = request.data.get('ingredients', [])
            for ingredient_data in ingredients_data:
                # Retrieve existing ingredient if available
                ingredient_name = ingredient_data.get('name')
                ingredient_quantity = ingredient_data.get('quantity', 0)
                existing_ingredient = Ingredients.objects.filter(Q(name=ingredient_name) & Q(quantity=ingredient_quantity)).first()

                if existing_ingredient:
                    # Use existing ingredient
                    recipe.ingredients.add(existing_ingredient)
                else:
                    # Create new ingredient if not found
                    new_ingredient = Ingredients.objects.create(name=ingredient_name, quantity=ingredient_quantity)
                    recipe.ingredients.add(new_ingredient)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
            summary="Posts when user likes the recipe",
            description="This endpoint is used for posting when user likes the recipe",
    )
    def post(self, request, *args, **kwargs):
        try:
            recipe = Recipe.objects.get(id=kwargs['pk'])
        except Recipe.DoesNotExist:
            return Response({"message": "Recipe not found"}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        # Check if the user has already liked the recipe
        if Like.objects.filter(user=user, recipe=recipe).exists():
            return Response({"message": "You have already liked this recipe"}, status=status.HTTP_400_BAD_REQUEST)

        # Create a like instance
        Like.objects.create(user=user, recipe=recipe)

        return Response({"message": "Recipe liked successfully"}, status=status.HTTP_201_CREATED)


class RecipeUnlikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
            summary="Posts when user cancels the like for recipe",
            description="This endpoint is used for posting when user cancels the like for recipe",
    )
    def post(self, request, *args, **kwargs):
        try:
            recipe = Recipe.objects.get(id=kwargs['pk'])
        except Recipe.DoesNotExist:
            return Response({"message": "Recipe not found"}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        # Check if the user has liked the recipe
        try:
            like = Like.objects.get(user=user, recipe=recipe)
        except Like.DoesNotExist:
            return Response({"message": "You have not liked this recipe"}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the like instance
        like.delete()

        return Response({"message": "Recipe unliked successfully"}, status=status.HTTP_200_OK)


class RecipeSaveAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
            summary="Posts when user saves recipe",
            description="This endpoint sends the user info who saved the recipe",
    )
    def post(self, request, *args, **kwargs):
        try:
            recipe = Recipe.objects.get(id=kwargs['pk'])
        except Recipe.DoesNotExist:
            return Response({"message": "Recipe not found"}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        # Check if the user has already saved the recipe
        if Save.objects.filter(user=user, recipe=recipe).exists():
            return Response({"message": "You have already saved this recipe"}, status=status.HTTP_400_BAD_REQUEST)

        # Create a saved recipe instance
        Save.objects.create(user=user, recipe=recipe)

        return Response({"message": "Recipe saved successfully"}, status=status.HTTP_201_CREATED)


class RecipeUnsaveAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
            summary="Posts when user cancels the save for the recipe",
            description="This endpoint sends the user cancels the save for the recipe",
    )
    def post(self, request, *args, **kwargs):
        try:
            recipe = Recipe.objects.get(id=kwargs['pk'])
        except Recipe.DoesNotExist:
            return Response({"message": "Recipe not found"}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        # Check if the user has saved the recipe
        try:
            saved_recipe = Save.objects.get(user=user, recipe=recipe)
        except Save.DoesNotExist:
            return Response({"message": "You have not saved this recipe"}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the saved recipe instance
        saved_recipe.delete()

        return Response({"message": "Recipe unsaved successfully"}, status=status.HTTP_200_OK)

