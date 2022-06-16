from textwrap import indent
from django.contrib import admin
from django.urls import path

from .views import index
from .views import generateMCExample
from .views import generateBinaryExpression
from .views import clozeText

urlpatterns = [
    path('', index),
    path('example/', generateMCExample),
    path('examplebin/', generateBinaryExpression),
    path('examplecloze/', clozeText),
]
