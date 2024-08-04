from rest_framework import serializers
from .models import Meal, Menu, AnimalProtein, VegetableProtein, Carbohydrate, RootVegetables, Vegetables, Herb, Seaweed, Fruit

class AnimalProteinSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = AnimalProtein
        fields = ['name']

class VegetableProteinSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = VegetableProtein
        fields = ['name']

class CarbohydrateSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Carbohydrate
        fields = ['name']

class RootVegetablesSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = RootVegetables
        fields = ['name']

class VegetablesSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Vegetables
        fields = ['name']

class HerbSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Herb
        fields = ['name']

class SeaweedSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Seaweed
        fields = ['name']

class FruitSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Fruit
        fields = ['name']

class MenuSerializer(serializers.ModelSerializer):
    animal_protein = AnimalProteinSerializer(many=True, read_only=True)
    vegetable_protein = VegetableProteinSerializer(many=True, read_only=True)
    carbohydrate = CarbohydrateSerializer(many=True, read_only=True)
    root_vegetables = RootVegetablesSerializer(many=True, read_only=True)
    vegetables = VegetablesSerializer(many=True, read_only=True)
    herb = HerbSerializer(many=True, read_only=True)
    seaweed = SeaweedSerializer(many=True, read_only=True)
    fruit = FruitSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = ['menu_name', 'animal_protein', 'vegetable_protein', 'carbohydrate', 'root_vegetables', 'vegetables', 'herb', 'seaweed', 'fruit']

class MealSerializer(serializers.ModelSerializer):
    morning = MenuSerializer(many=True, read_only=True)
    lunch = MenuSerializer(many=True, read_only=True)
    dinner = MenuSerializer(many=True, read_only=True)
    snack = MenuSerializer(many=True, read_only=True)
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Meal
        fields = ['id', 'morning', 'lunch', 'dinner', 'snack', 'date', 'user']
