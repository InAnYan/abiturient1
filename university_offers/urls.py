from django.urls import path


from . import views


urlpatterns = [
    path("offers/json", views.offers_json, name="offers_json"),
    path("offers/json_to_html", views.offers_json_to_html, name="offers_json_to_html"),
]
