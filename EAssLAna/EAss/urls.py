from django.contrib import admin
from django.urls import path

from .views import generateExample
from .views import generateBinaryExpression, clozeText

urlpatterns = [
    path('example/', generateExample),
    path('examplebin/', generateBinaryExpression),
    path('cloze/', clozeText)
]
