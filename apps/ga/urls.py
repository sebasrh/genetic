from django.urls import path
from apps.ga import views

urlpatterns = [
    path('', views.ga, name="ga"),
    path('generations/<int:generations_id>/',
         views.generations, name="generations"),
    path('generations/<int:generations_id>/evolve/', views.evolve, name="evolve"),
    path('generations/<int:generations_id>/evaluate/<int:melody_id>/', views.evaluate, name="evaluate"),

]
