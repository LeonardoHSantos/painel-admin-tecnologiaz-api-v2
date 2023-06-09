from . import views
from django.urls import path

urlpatterns = [
    path("autenticacao-iqoption/", views.autenticao_iqoption, name="autenticacao_iqoption"),
    path("start-api/", views.start_api, name="start_api"),
    path("stop-api/", views.stop_api, name="stop_api"),
]