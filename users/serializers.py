from rest_framework import serializers
from .models import User
from recipes.serializers import RecipeListAPI


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50, min_length=8, write_only=True)
    password_confirm = serializers.CharField(max_length=50, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password_confirm']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")

        if not username.isalnum:
            raise serializers.ValidationError('username should contain alphanumeric characters')

        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        return User.objects.create_user(**validated_data)


class UserActivationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50, min_length=8, write_only=True)
    username = serializers.CharField(max_length=255, min_length=5)

    class Meta:
        model = User
        fields = ['username', 'password']


class UsersListAPI(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'bio', 'image']


class UserProfileSerializer(serializers.ModelSerializer):
    my_recipes = serializers.SerializerMethodField()
    saved_recipes = serializers.SerializerMethodField()
    recipe_num = serializers.IntegerField(source='recipe.count', read_only=True)
    followers_num = serializers.IntegerField(source='followers.count', read_only=True)
    following_num = serializers.IntegerField(source='following.count', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'bio', 'image', 'my_recipes', 'saved_recipes', 'recipe_num', 'followers_num', 'following_num']

    def get_my_recipes(self, instance):
        recipes = instance.recipe.all()  # Corrected line
        return RecipeListAPI(recipes, many=True).data

    def get_saved_recipes(self, instance):
        saved_recipes = instance.saved_recipes.all()
        return RecipeListAPI(saved_recipes, many=True).data


class UserManageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'bio', 'image']








