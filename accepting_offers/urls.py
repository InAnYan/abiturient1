from django.urls import path

from . import views


urlpatterns = [
    path(
        "",
        views.AbiturientAndOffersWizard.as_view(),
        name="form",
    ),
    path("done", views.done, name="done"),
]
