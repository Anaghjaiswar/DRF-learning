from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Recipe
from .serializers import RecipeSerializer
from django.http import HttpResponse


def home(request):
    return HttpResponse('welcome to the Recipes API!')

@api_view(['GET','POST'])  #this decorator tells DRF that this view will handle GET requests
def recipe_list(request):
    if request.method == 'GET':
        #When a GET request is made, it returns the list of recipes.
        recipes = Recipe.objects.all() #retrieves all the Recipe objects from the databse
        serializer = RecipeSerializer(recipes, many = True) #serializes the listof recipes, the many = True argument tells DRF that you're serializing a list of objects(not just a single object)
        return Response(serializer.data) #Returns the serialized data in the HTTP response. DRF automatically converts the serializer.data into a JSON response.
    elif request.method == 'POST':
        # When a POST request is made, it attempts to create a new recipe using the data provided in the request.
        serializer = RecipeSerializer(data = request.data)  # creates a new serializer instance and passes the data from the incoming request.
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

