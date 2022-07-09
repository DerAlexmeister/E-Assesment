from django.contrib import admin
from django.urls import path

from .views import index
from .views import handleAssemblerAnalytics

urlpatterns = [
    path('', index, name="lahomeview"),
    path('assembleranalysis', handleAssemblerAnalytics),
]
