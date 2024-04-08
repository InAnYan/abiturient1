from django.urls import path


from . import views


urlpatterns = [
    path("ajax/specialities", views.ajax_specialities, name="ajax_specialities"),
    path("ajax/study_forms", views.ajax_study_forms, name="ajax_study_forms"),
    path("ajax/offer_types", views.ajax_offer_types, name="ajax_offer_types"),
    path("ajax/offer_info", views.ajax_offer_info, name="ajax_offer_info"),
]
