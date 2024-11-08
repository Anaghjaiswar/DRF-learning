from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .models import Recipe
from .serializers import RecipeSerializer
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsOwnerOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics


@api_view(['GET'])
@permission_classes([AllowAny])
def home(request):
    return Response({'message':'welcome to the Recipes API!'})

@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication]) # Use TokenAuthentication here
@permission_classes([IsAdminUser])
def admin_only_view(request):
    # Only accessible by admin users
    return Response({"message": "Admin content"})



@api_view(['GET','POST'])  #this decorator tells DRF that this view will handle GET requests
@permission_classes([IsAuthenticated])
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
        

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated,IsOwnerOrReadOnly])
def recipe_detail(request, pk):
    # Fetch the recipe by primary key (pk) or return a 404 error if not found
    recipe = get_object_or_404(Recipe, pk=pk)

    if request.method == 'GET':
        # Retrieve and return the recipe details
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        # Update the recipe details with the data from the request
        serializer = RecipeSerializer(recipe, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Delete the recipe and return a 204 No Content response
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def logout_view(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message":"successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
# list and create recipes
class RecipeListCreateView(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]


# Retrieve, update, or delete a single recipe
class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]