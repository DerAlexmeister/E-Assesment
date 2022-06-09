from django.contrib import admin
from django.urls import path

from .views import generateExample
from .views import generateBinaryExpression

urlpatterns = [
   path('example/', generateExample),
   path('examplebin/', generateBinaryExpression),
]
