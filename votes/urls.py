from django.urls import path
from votes import views, json_views

app_name = "votes"

urlpatterns = [
    path("", views.latest_votation_date, name="latest"),
    path("dates/<int:votation_date_id>/",
         views.votation_date_detail,
         name="votation_date_detail"),
    path("dates/", views.votation_date_list, name="votation_date_list"),
    path("votes/<int:votation_id>/", views.votation_detail, name="votation_detail"),
    path("votes/<int:votation_id>/stats/", views.votation_stats, name="votation_stats"),
    path("votes/<int:votation_id>/communes/",
         views.votation_communes,
         name="votation_communes"),
    path("votes/<int:votation_id>/canton/<int:canton_id>/",
         views.votation_canton_detail,
         name="votation_canton_detail"),
    path("json/dates/<int:votation_date_id>/",
         json_views.votation_date_json,
         name="votation_date_json"),
    path("votes/json/<int:votation_id>/",
         json_views.votation_canton_json,
         name="votation_canton_json"),
    path("votes/json/<int:votation_id>/communes/",
         json_views.votation_commune_json,
         name="votation_canton_json"),
    path("votes/json/<int:votation_id>/canton/<int:canton_id>/",
         json_views.votation_canton_commune_json,
         name="votation_canton_json"),
]
