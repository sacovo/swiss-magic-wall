from django.urls import path

from api import views

app_name = "api"

urlpatterns = [
    path("dates/", views.votation_date_list, name="votation_list"),
    path("dates/<int:votation_date_id>/",
         views.votation_date_detail,
         name="votation_date_detail"),
    path("votation/<int:votation_id>/", views.votation_detail, name="votation_detail"),
    path("votation/<int:votation_id>/stats/", views.votation_stats,
         name="votation_stats"),
    path("votation/<int:votation_id>/stats/<int:canton_id>/",
         views.votation_stats,
         name="votation_stats_canton"),
    path("votation/<int:votation_id>/stats/commune/<int:commune_id>/",
         views.votation_stats_commune,
         name="votation_stats_commune"),
    path("votation/<int:votation_id>/rel/", views.swiss_stats, name="related_results"),
    path("votation/<int:votation_id>/rel/canton/<int:canton_id>/",
         views.canton_stats,
         name="related_results_canton"),
    path("votation/<int:votation_id>/rel/commune/<int:commune_id>/",
         views.commune_stats,
         name="related_results_commune"),
]
