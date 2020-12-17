from django.urls import path
from geo import views

app_name = "geo"

urlpatterns = [
    path("", views.canton_list, name="canton_list"),
    path("canton/<int:canton_id>/", views.canton_detail, name="canton_detail"),
    path("commune/<int:canton_id>/", views.commune_detail, name="commune_detail"),
    path("canton/<int:canton_id>/json/", views.canton_json, name="canton_detail"),
    path("commune/<int:canton_id>/json/", views.commune_json, name="commune_detail"),
]
