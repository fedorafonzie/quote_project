"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
# quote_api/core/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from quotes_app.views import ModerationViewSet # Zorg dat de juiste viewset wordt geïmporteerd

# Maak een router aan
router = DefaultRouter()
router.register(r'moderation', ModerationViewSet, basename='moderation') # <-- REGISTREER

urlpatterns = [
    path('admin/', admin.site.urls),
    # Dit is de URL voor je bestaande API. We voegen de router hieraan toe.
    path('api/', include('quotes_app.urls')),
    path('api/', include(router.urls)), # <-- VOEG DE ROUTER URLS TOE
]