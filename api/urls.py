from django.urls import path

from api import views

app_name = "api"

urlpatterns = [
    path("dates/", views.votation_date_list, name="votation_list"),
    path("dates/<int:votation_date_id>/",
         views.votation_date_detail,
         name="votation_date_detail"),
    path("votation/<int:votation_id>/", views.votation_detail, name="votation_detail"),
]
