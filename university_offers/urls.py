from django.urls import path


from . import views


urlpatterns = [
    path("ajax/bases", views.ajax_bases, name="ajax_bases"),
    path("ajax/levels", views.ajax_levels, name="ajax_levels"),
    path("ajax/study_forms", views.ajax_study_forms, name="ajax_study_forms"),
    path("ajax/offer_types", views.ajax_offer_types, name="ajax_offer_types"),
    path("ajax/offer_info", views.ajax_offer_info, name="ajax_offer_info"),
]
