from textwrap import indent
from django.contrib import admin
from django.urls import path

from .views import index
from .views import generateMCExample
from .views import generateBinaryExpression
from .views import clozeText
from .views import generateMCQuestions
from .views import generateBinaryQuestions
from .views import generateOctaQuestions

urlpatterns = [
    ## Production
    path('', index),
    path('mcgenerator/', generateMCQuestions),
    path('bingenerator/', generateBinaryQuestions),
    path('octagenerator/', generateOctaQuestions),

    ## Examples 
    path('example/', generateMCExample),
    path('examplebin/', generateBinaryExpression),
    path('examplecloze/', clozeText),
]
