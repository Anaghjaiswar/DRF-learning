"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from api.views import home
from api.views import RecipeListCreateView,RecipeDetailView

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', home),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/token/',TokenObtainPairView.as_view(), name = 'token_obtain_pair'),  #login
    path('api/token/refresh/',TokenRefreshView.as_view(), name = 'token_refresh'),  #refresh token
    path('recipes/', RecipeListCreateView.as_view(), name='recipe-list-create'),
    path('recipes/<int:pk>/',RecipeDetailView.as_view(), name='recipe-detail'),
]


# token/: Endpoint to obtain the access and refresh token pair by providing valid credentials.
# token/refresh/: Endpoint to refresh an access token using a refresh token.