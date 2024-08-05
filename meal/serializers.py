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
    animal_protein = AnimalProteinSerializer(many=True)
    vegetable_protein = VegetableProteinSerializer(many=True)
    carbohydrate = CarbohydrateSerializer(many=True)
    root_vegetables = RootVegetablesSerializer(many=True)
    vegetables = VegetablesSerializer(many=True)
    herb = HerbSerializer(many=True)
    seaweed = SeaweedSerializer(many=True)
    fruit = FruitSerializer(many=True)

    class Meta:
        model = Menu
        fields = ['menu_name', 'animal_protein', 'vegetable_protein', 'carbohydrate', 'root_vegetables', 'vegetables', 'herb', 'seaweed', 'fruit']

    def create(self, validated_data):
        animal_proteins = validated_data.pop('animal_protein', [])
        vegetable_proteins = validated_data.pop('vegetable_protein', [])
        carbohydrates = validated_data.pop('carbohydrate', [])
        root_vegetables = validated_data.pop('root_vegetables', [])
        vegetables = validated_data.pop('vegetables', [])
        herbs = validated_data.pop('herb', [])
        seaweeds = validated_data.pop('seaweed', [])
        fruits = validated_data.pop('fruit', [])
        
        menu = Menu.objects.create(**validated_data)

        # Adding related fields
        menu.animal_protein.set([AnimalProtein.objects.get_or_create(name=item['name'])[0] for item in animal_proteins])
        menu.vegetable_protein.set([VegetableProtein.objects.get_or_create(name=item['name'])[0] for item in vegetable_proteins])
        menu.carbohydrate.set([Carbohydrate.objects.get_or_create(name=item['name'])[0] for item in carbohydrates])
        menu.root_vegetables.set([RootVegetables.objects.get_or_create(name=item['name'])[0] for item in root_vegetables])
        menu.vegetables.set([Vegetables.objects.get_or_create(name=item['name'])[0] for item in vegetables])
        menu.herb.set([Herb.objects.get_or_create(name=item['name'])[0] for item in herbs])
        menu.seaweed.set([Seaweed.objects.get_or_create(name=item['name'])[0] for item in seaweeds])
        menu.fruit.set([Fruit.objects.get_or_create(name=item['name'])[0] for item in fruits])

        return menu

class MealSerializer(serializers.ModelSerializer):
    morning = MenuSerializer(many=True)
    lunch = MenuSerializer(many=True)
    dinner = MenuSerializer(many=True)
    snack = MenuSerializer(many=True)
    user = serializers.CharField(source='user.username')

    class Meta:
        model = Meal
        fields = ['id', 'morning', 'lunch', 'dinner', 'snack', 'date', 'user']
