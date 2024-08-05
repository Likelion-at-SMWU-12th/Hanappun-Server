from django.db import models
from users.models import User

class BodyType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class AnimalProtein(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class VegetableProtein(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Carbohydrate(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class RootVegetables(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Vegetables(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Herb(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Seaweed(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Fruit(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Menu(models.Model):
    menu_name = models.CharField(max_length=100)
    animal_protein = models.ManyToManyField(AnimalProtein, blank=True)
    vegetable_protein = models.ManyToManyField(VegetableProtein, blank=True)
    carbohydrate = models.ManyToManyField(Carbohydrate, blank=True)
    root_vegetables = models.ManyToManyField(RootVegetables, blank=True)
    vegetables = models.ManyToManyField(Vegetables, blank=True)
    herb = models.ManyToManyField(Herb, blank=True)
    seaweed = models.ManyToManyField(Seaweed, blank=True)
    fruit = models.ManyToManyField(Fruit, blank=True)

    def __str__(self):
        return self.menu_name

class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    morning = models.ManyToManyField(Menu, related_name='morning_meals', blank=True)
    lunch = models.ManyToManyField(Menu, related_name='lunch_meals', blank=True)
    dinner = models.ManyToManyField(Menu, related_name='dinner_meals', blank=True)
    snack = models.ManyToManyField(Menu, related_name='snack_meals', blank=True)

    def __str__(self):
        return f'{self.user} - {self.date}'

