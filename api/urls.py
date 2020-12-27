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
]
