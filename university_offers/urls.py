from django.urls import path


from . import views


urlpatterns = [
    path("ajax/offers", views.ajax_offers, name="ajax_offers"),
]
