from django.urls import path

from abiturients import views


urlpatterns = [
    path("ajax/birth_country/", views.birth_country, name="ajax_birth_country"),
    path("ajax/birth_town/", views.birth_town, name="ajax_birth_town"),
    path("ajax/nationality/", views.nationality, name="ajax_nationality"),
    path(
        "ajax/foreign_language/", views.foreign_language, name="ajax_foreign_language"
    ),
]
