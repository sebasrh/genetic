from django.urls import path
from apps.home import views
from django.conf.urls import handler404

from apps.home.views import page_not_found

urlpatterns = [
    path('', views.home, name="home"),
]

handler404 = page_not_found
