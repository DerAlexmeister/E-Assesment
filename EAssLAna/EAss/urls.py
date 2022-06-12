from django.contrib import admin
from django.urls import path

from .views import generateMCExample
from .views import generateBinaryExpression

urlpatterns = [
   path('examplemc/', generateMCExample),
   path('examplebin/', generateBinaryExpression),
]
